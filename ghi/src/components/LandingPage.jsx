import { useState } from 'react';
import { useLoginMutation, useSignupMutation } from '/src/api/profApi';
import { useDispatch } from 'react-redux';
import { profApi } from '/src/api/profApi';
import { useAuthToken } from '../features/tokenSelector';
import { setToken } from '../features/authTokenSlice';

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
    //   try {
        const response = await signup({ username, name, email, password })
        // Handle successful signup
        console.log('Signed up successfully');
        console.log(response)
        dispatch(setToken(response.data))
    //   } catch (error) {
    //     // Handle signup error
    //     console.error('Signup error:', error);
    //   }
    } else {
      try {
        const response = await login({ email, password })
        // Handle successful login
        console.log(response)
        dispatch(setToken(response.data))
        console.log('Logged in successfully');
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

  const handleLogout = async (event) => {
    event.preventDefault()
    localStorage.removeItem('token');
    dispatch(profApi.util.invalidateTags('User'))
  };

  return (
    <div className="landing-page">
      {token ? (
        <div>
          <h2>Welcome, {token.user.name}!</h2>
          <button className='btn btn-warning' onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <>
          <h2>{isSignUp ? 'Sign Up' : 'Login'}</h2>
          <form>
            {isSignUp && (
              <>
                <label className='form-label'>
                  Username:
                  <input className='form-control' type="text" value={username} onChange={(event) => setUsername(event.target.value)} />
                </label>
                <br />
                <label className='form-label'>
                  Name:
                  <input className='form-control' type="text" value={name} onChange={(event) => setName(event.target.value)} />
                </label>
                <br />
              </>
            )}
            <label className='form-label'>
              Email:
              <input className='form-control' type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
            </label>
            <br />
            <label className='form-label'>
              Password:
              <input className='form-control' type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
            </label>
            <br />
            {isSignUp && (
              <button className='btn btn-warning' onClick={handleSubmit}>Sign Up</button>
            )}
            {!isSignUp && (
              <button className='btn btn-warning' onClick={handleSubmit}>Login</button>
            )}
            <br />
            <button className='btn btn-warning' onClick={handleSwitchForm}>
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
