/* eslint-disable react/prop-types */

function AppCard({ app }) {
    return (
        <div className="card">
            <img className="card-img-top" src={app.image} alt={app.name} height="100" />
            <div className="card-body">
                <h3 className="card-title">{app.name}</h3>
                <a className="btn btn-warning" href={app.url}>Visit</a>
            </div>
        </div>
    );
}

export default AppCard;
