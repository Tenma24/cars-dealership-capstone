import React, {useState} from 'react';
import {api} from '../../api';
export default function Register() {
  const [error,setError]=useState(''); const [busy,setBusy]=useState(false);
  async function submit(event) {
    event.preventDefault();setBusy(true);setError('');
    try { await api('register',Object.fromEntries(new FormData(event.currentTarget)));window.location.href='/dealers'; }
    catch(error) {setError(error.message);setBusy(false);}
  }
  return <section className="auth card"><p className="eyebrow">JOIN THE COMMUNITY</p><h1>A better journey starts here.</h1><p className="muted">Create an account to share your dealership experience.</p><form onSubmit={submit}>
    <label>Username<input name="userName" autoComplete="username" required maxLength="150"/></label>
    <div className="two"><label>First Name<input name="firstName" autoComplete="given-name" required maxLength="150"/></label><label>Last Name<input name="lastName" autoComplete="family-name" required maxLength="150"/></label></div>
    <label>Email<input name="email" type="email" autoComplete="email" required maxLength="254"/></label>
    <label>Password<input name="password" type="password" autoComplete="new-password" required minLength="8" maxLength="128"/></label><small>Use at least 8 characters and avoid common passwords.</small>
    {error&&<p role="alert" className="error">{error}</p>}<button disabled={busy}>{busy?'Creating account…':'Register'}</button>
  </form><p>Already a member? <a href="/login">Log in</a></p></section>;
}
