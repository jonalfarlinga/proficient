import AppCard from "./AppCard.jsx";

function Dashboard() {
    const apps = [
      { name: 'App 1', image: 'https://via.placeholder.com/100', url: 'https://www.example.com/app1' },
      { name: 'App 2', image: 'https://via.placeholder.com/100', url: 'https://www.example.com/app2' },
      { name: 'App 3', image: 'https://via.placeholder.com/100', url: 'https://www.example.com/app3' },
    ];

    return (
      <div className="dashboard">
        <h2>Dashboard</h2>
        <ul className="app-list">
          {apps.map((app, index) => (
            <li key={index}>
              <AppCard app={app} />
            </li>
          ))}
        </ul>
      </div>
    );
}

export default Dashboard;
