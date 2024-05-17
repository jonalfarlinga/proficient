function Profile() {
  // Replace this with your actual user data
  const userData = {
    name: 'John Doe',
    email: 'john.doe@example.com',
    profilePicture: 'https://via.placeholder.com/100',
  };

  return (
    <div className="profile">
      <h2>Profile</h2>
      <img src={userData.profilePicture} alt={userData.name} />
      <h3>{userData.name}</h3>
      <p>Email: {userData.email}</p>
    </div>
  );
}

export default Profile;
