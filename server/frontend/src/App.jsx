import React, { useEffect, useState } from "react";
import { api } from "./api";
import Register from "./components/Register/Register";

function Login() {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    try {
      await api("login", Object.fromEntries(new FormData(event.currentTarget)));
      window.location.href = "/dealers";
    } catch (e) {
      setError(e.message);
      setBusy(false);
    }
  }
  return (
    <section className="auth card">
      <p className="eyebrow">WELCOME BACK</p>
      <h1>Your next chapter.</h1>
      <p className="muted">Log in to review your dealership.</p>
      <form onSubmit={submit}>
        <label>
          Username
          <input name="userName" required autoComplete="username" />
        </label>
        <label>
          Password
          <input
            name="password"
            type="password"
            required
            autoComplete="current-password"
          />
        </label>
        {error && (
          <p role="alert" className="error">
            {error}
          </p>
        )}
        <button disabled={busy}>{busy ? "Logging in…" : "Log in"}</button>
      </form>
      <p>
        New here? <a href="/register">Create an account</a>
      </p>
    </section>
  );
}
function Dealers({ user }) {
  const [all, setAll] = useState(null);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [state, setState] = useState(
    new URLSearchParams(location.search).get("state") || "",
  );
  useEffect(() => {
    api("get_dealers")
      .then((r) => setAll(r.dealers))
      .catch((e) => setError(e.message));
  }, []);
  const filtered = (all || []).filter(
    (d) =>
      (!state || d.state === state) &&
      `${d.full_name} ${d.city}`.toLowerCase().includes(search.toLowerCase()),
  );
  function changeState(value) {
    setState(value);
    history.replaceState(
      null,
      "",
      "/dealers" + (value ? "?state=" + encodeURIComponent(value) : ""),
    );
  }
  return (
    <>
      <section className="hero">
        <div>
          <p className="eyebrow">GOOD PEOPLE. GREAT DRIVES.</p>
          <h1>
            Find your next
            <br />
            <em>chapter.</em>
          </h1>
          <p>
            Explore dealerships across the country.
            <br />
            Real experiences. A more confident choice.
          </p>
          <a className="button light" href="#directory">
            Explore dealerships <span>↗</span>
          </a>
        </div>
        <img
          src="/static/car_dealership.jpg"
          alt="Cars ready for their next owners at a dealership"
        />
        <div className="hero-note">THE ROAD AHEAD STARTS HERE</div>
      </section>
      <section id="directory" className="directory">
        <div className="section-title">
          <div>
            <p className="eyebrow">THE DEALERSHIP DIRECTORY</p>
            <h2>A great drive starts locally.</h2>
          </div>
          <span className="count">
            {all ? all.length : "…"} locations nationwide
          </span>
        </div>
        <div className="filters">
          <label>
            Search dealerships
            <input
              type="search"
              placeholder="Dealership or city"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </label>
          <label>
            Filter by state
            <select value={state} onChange={(e) => changeState(e.target.value)}>
              <option value="">All states</option>
              {[...new Set((all || []).map((d) => d.state))].sort().map((s) => (
                <option key={s}>{s}</option>
              ))}
            </select>
          </label>
          <p>{filtered.length} dealerships found</p>
        </div>
        {error ? (
          <p role="alert" className="error">
            {error}
          </p>
        ) : !all ? (
          <p role="status">Loading dealerships…</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>DEALERSHIP</th>
                  <th>CITY</th>
                  <th>STATE</th>
                  <th>ADDRESS</th>
                  <th>EXPLORE</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((d) => (
                  <tr key={d.id}>
                    <td>
                      <a className="dealer-name" href={"/dealer/" + d.id}>
                        {d.full_name}
                      </a>
                      <small>LOCATION {String(d.id).padStart(3, "0")}</small>
                    </td>
                    <td>{d.city}</td>
                    <td>
                      <span className="pill">{d.state}</span>
                    </td>
                    <td>{d.address}</td>
                    <td>
                      <a href={"/dealer/" + d.id}>View reviews ↗</a>
                      {user && (
                        <a className="review-link" href={"/postreview/" + d.id}>
                          Review Dealer
                        </a>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!filtered.length && (
              <p className="empty">
                No dealerships match your search. Try another city or state.
              </p>
            )}
          </div>
        )}
      </section>
    </>
  );
}
function Dealer({ id, user }) {
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    Promise.all([api("dealer/" + id), api("reviews/dealer/" + id)])
      .then(([d, r]) => {
        setDealer(d.dealer);
        setReviews(r.reviews);
      })
      .catch((e) => setError(e.message));
  }, [id]);
  if (error)
    return (
      <p role="alert" className="error">
        {error}
      </p>
    );
  if (!dealer) return <p role="status">Loading dealership…</p>;
  return (
    <section className="detail">
      <a href="/dealers">← All dealerships</a>
      <div className="detail-head">
        <div>
          <p className="eyebrow">
            {dealer.city.toUpperCase()} · {dealer.state.toUpperCase()}
          </p>
          <h1>{dealer.full_name}</h1>
          <p>
            {dealer.address}, {dealer.city}, {dealer.st} {dealer.zip}
          </p>
        </div>
        <a className="button" href={user ? "/postreview/" + id : "/login"}>
          {user ? "Review Dealer" : "Log in to review"} ↗
        </a>
      </div>
      <img
        className="detail-image"
        src="/static/cars.jpeg"
        alt="Cars on display"
      />
      <div className="section-title">
        <h2>Customer experiences</h2>
        <span className="count">{reviews.length} reviews</span>
      </div>
      <div className="reviews">
        {reviews.map((r) => (
          <article className="card review" key={r.id}>
            <div className="review-head">
              <strong>{r.name}</strong>
              <span className={"sentiment " + r.sentiment}>{r.sentiment}</span>
            </div>
            <p className="review-text">{r.review}</p>
            {r.purchase && (
              <small>
                {r.car_year} {r.car_make} {r.car_model} · Purchased{" "}
                {r.purchase_date}
              </small>
            )}
          </article>
        ))}
      </div>
      {!reviews.length && (
        <p className="empty">
          Be the first to share an experience at this dealership.
        </p>
      )}
    </section>
  );
}
function PostReview({ id, user }) {
  const [dealer, setDealer] = useState(null);
  const [makes, setMakes] = useState([]);
  const [purchase, setPurchase] = useState(false);
  const [make, setMake] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    Promise.all([api("dealer/" + id), api("get_cars")])
      .then(([d, c]) => {
        setDealer(d.dealer);
        setMakes(c.car_makes);
      })
      .catch((e) => setError(e.message));
  }, [id]);
  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const data = Object.fromEntries(new FormData(e.currentTarget));
    try {
      await api("add_review", {
        ...data,
        dealership: Number(id),
        purchase,
        car_model_id: Number(data.car_model_id),
      });
      location.href = "/dealer/" + id;
    } catch (e) {
      setError(e.message);
      setBusy(false);
    }
  }
  if (!user)
    return (
      <section className="auth card">
        <h1>Share your experience.</h1>
        <p>Please log in before posting a review.</p>
        <a className="button" href="/login">
          Log in
        </a>
      </section>
    );
  return (
    <section className="auth card wide">
      <p className="eyebrow">YOUR EXPERIENCE MATTERS</p>
      <h1>Post a review</h1>
      <p className="muted">{dealer?.full_name || "Loading dealership…"}</p>
      <form onSubmit={submit}>
        <label>
          Your review
          <textarea
            name="review"
            placeholder="Tell us about your visit…"
            required
            maxLength="2000"
            rows="5"
          />
        </label>
        <label className="check">
          <input
            type="checkbox"
            checked={purchase}
            onChange={(e) => setPurchase(e.target.checked)}
          />
          I purchased a vehicle
        </label>
        {purchase && (
          <>
            <div className="two">
              <label>
                Car make
                <select
                  required
                  value={make}
                  onChange={(e) => setMake(e.target.value)}
                >
                  <option value="">Select a make</option>
                  {makes.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Car model / year
                <select name="car_model_id" key={make} required defaultValue="">
                  <option value="">Select a model</option>
                  {(makes.find((m) => String(m.id) === make)?.models || []).map(
                    (m) => (
                      <option key={m.id} value={m.id}>
                        {m.name} · {m.year}
                      </option>
                    ),
                  )}
                </select>
              </label>
            </div>
            <label>
              Purchase date
              <input
                name="purchase_date"
                type="date"
                required
                max={new Date().toLocaleDateString("en-CA")}
              />
            </label>
          </>
        )}
        {error && (
          <p role="alert" className="error">
            {error}
          </p>
        )}
        <button disabled={busy || !dealer}>
          {busy ? "Posting…" : "Post review"}
        </button>
      </form>
    </section>
  );
}
export default function App() {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    api("session")
      .then((r) => {
        setUser(r.userName);
        setReady(true);
      })
      .catch((e) => setError(e.message));
  }, []);
  async function exit() {
    try {
      await api("logout", {});
      setUser(null);
      location.href = "/dealers";
    } catch (e) {
      setError(e.message);
    }
  }
  const path = location.pathname;
  const id = path.split("/")[2];
  return (
    <>
      <header>
        <a className="brand" href="/">
          C<span>↗</span>{" "}
          <b>
            CARS<span>DEALERSHIP</span>
          </b>
        </a>
        <nav aria-label="Main navigation">
          <a
            className={path === "/" || path === "/dealers" ? "active" : ""}
            href="/dealers"
          >
            Dealerships
          </a>
          <a href="/about/">About Us</a>
          <a href="/contact/">Contact Us</a>
        </nav>
        <div className="account">
          {user ? (
            <>
              <span className="username">{user}</span>
              <button className="outline" onClick={exit}>
                Log out
              </button>
            </>
          ) : (
            <>
              <a href="/login">Log in</a>
              <a className="button small" href="/register">
                Sign up ↗
              </a>
            </>
          )}
        </div>
      </header>
      <main>
        {error ? (
          <p className="error" role="alert">
            {error}
          </p>
        ) : !ready ? (
          <p role="status">Loading…</p>
        ) : path === "/register" ? (
          <Register />
        ) : path === "/login" ? (
          <Login />
        ) : path.startsWith("/postreview/") ? (
          <PostReview id={id} user={user} />
        ) : path.startsWith("/dealer/") ? (
          <Dealer id={id} user={user} />
        ) : (
          <Dealers user={user} />
        )}
      </main>
      <footer>
        <b>CARS DEALERSHIP</b>
        <span>Good people. Great drives.</span>
        <span>IBM full-stack capstone · Educational demo</span>
      </footer>
    </>
  );
}
