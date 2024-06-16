import AppCard from "./AppCard.jsx";

function Dashboard() {
    const apps = [
      { name: 'PDiF', image: '/pdiff.png', desc: "A simple utility for diffing PDFs.", url: 'https://pdiff.proficientdr.com' },
      { name: 'Calends', image: '/Calends.webp', desc: "A syllabus-builder for college classes. Calends builds a calendar for you.", url: 'https://calends.proficientdr.com' },
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
