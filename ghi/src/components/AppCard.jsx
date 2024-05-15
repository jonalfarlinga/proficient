/* eslint-disable react/prop-types */

function AppCard({ app }) {
    return (
        <div className="app-card">
        <img src={app.image} alt={app.name} />
        <h3>{app.name}</h3>
        <a href={app.url}>Visit</a>
        </div>
    );
}

export default AppCard;
