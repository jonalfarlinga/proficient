import { useState } from 'react';
import { useLoginMutation, useSignupMutation } from '/src/api/profApi';
import { useDispatch } from 'react-redux';
import { profApi } from '/src/api/profApi';
import { useAuthToken } from '/src/features/tokenSelector';
import { setToken, clearToken } from '/src/features/authTokenSlice';

function LandingPage() {
  const dispatch = useDispatch();
  const token = useAuthToken();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [name, setName] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [login, { isLoading: isLoginLoading, error: loginError }] = useLoginMutation();
  const [signup, { isLoading: isSignupLoading, error: signupError }] = useSignupMutation();

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (isSignUp) {
      try {
        const response = await signup({ username, name, email, password }).unwrap();
        // Handle successful signup
        console.log('Signed up successfully');
        dispatch(setToken(response))
      } catch (error) {
        // Handle signup error
        console.error('Signup error:', error);
      }
    } else {
      try {
        const response = await login({ email, password }).unwrap();
        // Handle successful login
        console.log('Logged in successfully');
        dispatch(setToken(response))
      } catch (error) {
        // Handle login error
        console.error('Login error:', error);
      }
    }
    setUsername('')
    setPassword('')
  };

  const handleSwitchForm = (event) => {
    event.preventDefault();
    setIsSignUp(!isSignUp);
  };

  const handleLogout = async () => {
    localStorage.removeItem('user');
    dispatch(profApi.util.invalidateTags('user'))
    dispatch(clearToken())
  };

  return (
    <div className="landing-page">
      {token ? (
        <div>
          <h2>Welcome, {token.user.name}!</h2>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <>
          <h2>{isSignUp ? 'Sign Up' : 'Login'}</h2>
          <form>
            {isSignUp && (
              <>
                <label>
                  Username:
                  <input type="text" value={username} onChange={(event) => setUsername(event.target.value)} />
                </label>
                <br />
                <label>
                  Name:
                  <input type="text" value={name} onChange={(event) => setName(event.target.value)} />
                </label>
                <br />
              </>
            )}
            <label>
              Email:
              <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
            </label>
            <br />
            <label>
              Password:
              <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
            </label>
            <br />
            {isSignUp && (
              <button onClick={handleSubmit}>Sign Up</button>
            )}
            {!isSignUp && (
              <button onClick={handleSubmit}>Login</button>
            )}
            <br />
            <button onClick={handleSwitchForm}>
              {isSignUp ? 'Already have an account? Login' : 'Create an account'}
            </button>
            {isLoginLoading || isSignupLoading ? (
              <p>Loading...</p>
            ) : null}
            {loginError || signupError ? (
              <p style={{ color: 'red' }}>
                {loginError?.data?.message || signupError?.data?.message}
              </p>
            ) : null}
          </form>
        </>
      )}
    </div>
  );
}
export default LandingPage;
