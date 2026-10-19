const express = require('express');
const { MongoClient } = require('mongodb');
const { rateLimit } = require('express-rate-limit');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const app=express();
app.disable('x-powered-by');
app.use(express.json({limit:'16kb'}));
app.use(rateLimit({windowMs:60000,limit:300}));
const seed=JSON.parse(fs.readFileSync(path.join(__dirname,'data/dealerships.json'))).dealerships;
const seedReviews=JSON.parse(fs.readFileSync(path.join(__dirname,'data/reviews.json'))).reviews;
let dealers, reviews, client;
const localFile=process.env.LOCAL_DATA_FILE || path.join(__dirname,'.local-reviews.json');
const fileMode=process.env.DATA_MODE==='file';
async function start() {
  if(fileMode) {
    dealers=seed;
    reviews=fs.existsSync(localFile)?JSON.parse(fs.readFileSync(localFile)):seedReviews;
    console.log('Explicit local file mode. Docker uses MongoDB.');
  } else {
    if(!process.env.MONGODB_URL) throw new Error('Set MONGODB_URL or DATA_MODE=file for local development');
    client=new MongoClient(process.env.MONGODB_URL);
    await client.connect();
    const db=client.db('dealershipsDB'); dealers=db.collection('dealers'); reviews=db.collection('reviews');
    await dealers.createIndex({id:1},{unique:true});
    await reviews.createIndex({id:1},{unique:true});
    await reviews.createIndex({dealership:1});
    await dealers.bulkWrite(seed.map(row=>({updateOne:{filter:{id:row.id},update:{$setOnInsert:row},upsert:true}})));
    await reviews.bulkWrite(seedReviews.map(row=>({updateOne:{filter:{id:row.id},update:{$setOnInsert:row},upsert:true}})));
  }
  if(!process.env.SERVICE_TOKEN) throw new Error('SERVICE_TOKEN is required for review writes');
  return app.listen(process.env.PORT||3030,process.env.HOST||'127.0.0.1',()=>console.log('Dealership service ready'));
}
async function find(collection,filter={}) {
  return fileMode?collection.filter(row=>Object.entries(filter).every(([key,value])=>row[key]===value)):collection.find(filter,{projection:{_id:0}}).toArray();
}
app.get('/health',(req,res)=>res.json({status:'ok',storage:fileMode?'file':'mongodb'}));
app.get('/fetchDealers',async(req,res)=>res.json(await find(dealers)));
app.get('/fetchDealers/:state',async(req,res)=>res.json(await find(dealers,{state:req.params.state})));
app.get('/fetchDealer/:id',async(req,res)=>res.json((await find(dealers,{id:Number(req.params.id)}))[0]||null));
app.get('/fetchReviews',async(req,res)=>res.json(await find(reviews)));
app.get('/fetchReviews/dealer/:id',async(req,res)=>res.json(await find(reviews,{dealership:Number(req.params.id)})));
app.post('/insert_review',async(req,res)=>{
  const expected=Buffer.from(process.env.SERVICE_TOKEN||'');
  const actual=Buffer.from(req.get('X-Service-Token')||'');
  if(!expected.length || actual.length!==expected.length || !crypto.timingSafeEqual(expected,actual)) return res.status(403).json({error:'Forbidden'});
  const data=req.body;
  if(!data || !Number.isInteger(data.dealership) || typeof data.review!=='string' || !data.review.trim() || data.review.length>2000 || typeof data.name!=='string' || data.name.length>300 || typeof data.purchase!=='boolean' || !['positive','neutral','negative'].includes(data.sentiment)) return res.status(400).json({error:'Invalid review'});
  if(!(await find(dealers,{id:data.dealership})).length) return res.status(404).json({error:'Dealer not found'});
  const row={id:crypto.randomUUID()};
  for(const key of ['dealership','review','name','username','purchase','purchase_date','car_make','car_model','car_year','sentiment']) if(data[key]!==undefined) row[key]=data[key];
  if(fileMode) {
    const next=[...reviews,row];
    fs.writeFileSync(localFile+'.tmp',JSON.stringify(next)); fs.renameSync(localFile+'.tmp',localFile); reviews=next;
  } else await reviews.insertOne({...row});
  res.status(201).json(row);
});
app.use((err,req,res,next)=>res.status(err.status===400?400:500).json({error:err.status===400?'Invalid JSON':'Service error'}));
if(require.main===module) start().catch(error=>{console.error(error.message);process.exit(1)});
async function closeDatabase() { if(client) await client.close(); }
module.exports={app,start,closeDatabase};
