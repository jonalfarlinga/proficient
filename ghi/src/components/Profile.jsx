import { useState } from 'react';
import { useUpdateUserMutation, useChangePasswordMutation } from '/src/api/profApi';
import { useDispatch } from 'react-redux';
import { useAuthToken } from '/src/features/tokenSelector';

function Profile() {
  const token = useAuthToken();
  const [name, setName] = useState(token ? token.user.name : '');
  const [username, setUsername] = useState(token ? token.user.username : '');
  const [email, setEmail] = useState(token ? token.user.email : '');
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [isEditingName, setIsEditingName] = useState(false);
  const [isEditingUsername, setIsEditingUsername] = useState(false);
  const [isEditingEmail, setIsEditingEmail] = useState(false);
  const [updateUser, { isLoading: isUpdateLoading, error: updateError }] = useUpdateUserMutation();
  const [changePassword, { isLoading: isChangePasswordLoading, error: changePasswordError }] = useChangePasswordMutation();

  const handleUpdateUser = async (event) => {
    event.preventDefault();

    try {
      const response = await updateUser({ name, username, email }).unwrap();
      // Handle successful user update
      console.log('User updated successfully');
    } catch (error) {
      // Handle user update error
      console.error('User update error:', error);
    }
  };

  const handleChangePassword = async (event) => {
    event.preventDefault();

    if (newPassword !== confirmNewPassword) {
      alert('New passwords do not match');
      return;
    }

    try {
      const response = await changePassword({ oldPassword, newPassword }).unwrap();
      // Handle successful password change
      console.log('Password changed successfully');
    } catch (error) {
      // Handle password change error
      console.error('Password change error:', error);
    }
  };
  if (!token) {
    return (<p>Loading...</p>)
  }
  return (
    <div className="profile">
      <h2>Profile</h2>
      <form>
        <div className='container d-flex'>
          <div className='w-25'>
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
          <div className='w-25'>
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
          <div className='w-25'>
            <label className='form-label'>
              Email:<br/>
                {isEditingEmail ? (
                  <input className='form-control' type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
                ) : (
                  <span>{email}</span>
                )}
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
      <form>
        <label className='form-label'>
          Old Password:
          <input className='form-control' type="password" value={oldPassword} onChange={(event) => setOldPassword(event.target.value)} />
        </label>
        <br />
        <label className='form-label'>
          New Password:
          <input className='form-control' type="password" value={newPassword} onChange={(event) => setNewPassword(event.target.value)} />
        </label>
        <br />
        <label className='form-label'>
          Confirm New Password:
          <input className='form-control' type="password" value={confirmNewPassword} onChange={(event) => setConfirmNewPassword(event.target.value)} />
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
  );
}


export default Profile;
