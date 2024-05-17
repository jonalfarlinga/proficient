import AppCard from "./AppCard.jsx";

function Dashboard() {
    const apps = [
      { name: 'App 1', image: '...', url: 'https://www.example.com/app1' },
      { name: 'App 2', image: '...', url: 'https://www.example.com/app2' },
      { name: 'App 3', image: '...', url: 'https://www.example.com/app3' },
    ];

    return (
      <div className="dashboard">
        <h2>Dashboard</h2>
        <div className="container row app-list">
            <div className='row row-cols-3'>
                {apps.map((app, index) => (
                    <AppCard app={app} key={index} />
                ))}
          </div>
        </div>
      </div>
    );
}

export default Dashboard;
