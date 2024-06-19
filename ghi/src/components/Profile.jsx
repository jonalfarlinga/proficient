import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUpdateUserMutation, useChangePasswordMutation } from '/src/api/profApi';
import { useAuthToken } from '/src/features/tokenSelector';
import { useDispatch } from 'react-redux';
import { clearToken, setToken } from '../features/authTokenSlice';

function Profile() {
    const dispatch = useDispatch()
    const navigate = useNavigate()
  const token = useAuthToken();
  useEffect (()=> {
    if (!token) {
        navigate('/');
    }
  }, [token, navigate]);
  const [name, setName] = useState(token ? token.user.name : '');
  const [username, setUsername] = useState(token ? token.user.username : '');
  const [email, setEmail] = useState(token ? token.user.email : '');
  const [updatePassword, setUpdatePassword] = useState('')
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [isEditingName, setIsEditingName] = useState(false);
  const [isEditingUsername, setIsEditingUsername] = useState(false);
  const [isEditingEmail, setIsEditingEmail] = useState(false);
  const [updateUser, { isLoading: isUpdateLoading, error: updateError }] = useUpdateUserMutation();
  const [changePassword, { isLoading: isChangePasswordLoading, error: changePasswordError }] = useChangePasswordMutation();

  const resetData = () => {
    setName(token.user.name);
    setUsername(token.user.username);
    setEmail(token.user.email);
    setUpdatePassword('');
    setOldPassword('');
    setNewPassword('');
    setConfirmNewPassword('');
    setIsEditingEmail(false);
    setIsEditingName(false);
    setIsEditingUsername(false);
  }

  useEffect(()=> {
    setName(token ? token.user.name: null);
    setUsername(token ? token.user.username: null);
    setEmail(token ? token.user.email: null);
    setUpdatePassword('');
    setOldPassword('');
    setNewPassword('');
    setConfirmNewPassword('');
    setIsEditingEmail(false);
    setIsEditingName(false);
    setIsEditingUsername(false);
  }, [token])

  const handleUpdateUser = async (event) => {
    event.preventDefault();

    try {
      const response = await updateUser({
        name,
        username,
        email,
        password: updatePassword
    }).unwrap()
      dispatch(setToken({
        user: response,
        access_token: token.access_token,
        token_type: token.token_type,
    }))
      console.log('User updated successfully');
    } catch (error) {
      console.log(error)
      alert(`User update error: ${error.status}\n` + error.data.detail);
    }
    resetData();
  };

  const handleChangePassword = async (event) => {
    event.preventDefault();

    if (newPassword !== confirmNewPassword) {
      alert('New passwords do not match');
      return;
    }

    try {
      await changePassword({
        password: oldPassword,
        new_password: newPassword,
        username: token.user.username,
        name: token.user.name,
        email: token.user.email,
      }).unwrap()
      dispatch(clearToken())
      alert('Password changed successfully! Please log in with the new password.');
      navigate('/')
    } catch (error) {
      alert(`User update error: ${error.status}\n` + error.data.detail);
    }
  };

  return (
    <>
    { token && (
    <div className="profile">
      <h2>Profile</h2>
      <h3>Update User Data</h3>
      <form>
        <div className='container d-flex'>
          <div className='em20'>
            <label className='form-label'>
              Name:<br/>
                {isEditingName ? (
                  <input className='form-control' type="text" value={name} onChange={(event) => setName(event.target.value)} />
                ) : (
                  <span>{name}</span>
                )}
            </label>
          </div>
          <div>
            <button onClick={(event) => {
              event.preventDefault();
              setIsEditingName(!isEditingName);
            }}>Edit</button>
          </div>
        </div>
        <div className='container d-flex'>
          <div className='em20'>
            <label className='form-label'>
              Username:<br/>
                {isEditingUsername ? (
                  <input className='form-control' type="text" value={username} onChange={(event) => setUsername(event.target.value)} />
                ) : (
                  <span>{username}</span>
                )}
            </label>
          </div>
          <div>
            <button onClick={(event) => {
              event.preventDefault();
              setIsEditingUsername(!isEditingUsername);
            }}>Edit</button>
          </div>
        </div>
        <div className='container d-flex'>
          <div className='em20'>
            <label className='form-label'>
              Email:<br/>
                {isEditingEmail ? (
                  <input className='form-control' type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
                ) : (
                  <span>{email}</span>
                )}
            </label>
            <label className='form-label'>
                Password:
              <input className='form-control' type="password" value={updatePassword} onChange={(event) => setUpdatePassword(event.target.value)} required />
            </label>
          </div>
          <div>
            <button onClick={(event) => {
              event.preventDefault();
              setIsEditingEmail(!isEditingEmail);
            }}>Edit</button>
          </div>
        </div>
        <br />
        <button className='btn btn-warning' onClick={handleUpdateUser}>Update User</button>
        {isUpdateLoading ? (
          <p>Loading...</p>
        ) : null}
        {updateError ? (
          <p style={{ color: 'red' }}>
            {updateError?.data?.message}
          </p>
        ) : null}
      </form>
      <hr />
      <h3>Change Password</h3>
      <form>
        <label className='form-label'>
          Old Password:
          <input className='form-control' type="password" value={oldPassword} onChange={(event) => setOldPassword(event.target.value)} required />
        </label>
        <br />
        <label className='form-label'>
          New Password:
          <input className='form-control' type="password" value={newPassword} onChange={(event) => setNewPassword(event.target.value)} required />
        </label>
        <br />
        <label className='form-label'>
          Confirm New Password:
          <input className='form-control' type="password" value={confirmNewPassword} onChange={(event) => setConfirmNewPassword(event.target.value)} required />
        </label>
        <br />
        <button className='btn btn-warning' onClick={handleChangePassword}>Change Password</button>
        {isChangePasswordLoading ? (
          <p>Loading...</p>
        ) : null}
        {changePasswordError ? (
          <p style={{ color: 'red' }}>
            {changePasswordError?.data?.message}
          </p>
        ) : null}
      </form>
    </div>
  )}
  </>
  );
}


export default Profile;
