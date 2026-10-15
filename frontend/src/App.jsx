import './App.css'

function App() {
  return (
    <div className="app">
      <header className="header">
        <div className="header-top">
          <span className="city">[Tu ciudad]</span>
          <button className="icon-btn" aria-label="Notificaciones">🔔</button>
        </div>

        <div className="search">
          <input placeholder="Buscá locales y prendas" />
          <button aria-label="Buscar por imagen">📷</button>
        </div>

        <div className="banner">
          <small>Cada compra suma</small>
          <h1>Ofertas de hoy en locales de ropa</h1>
          <button className="banner-btn">Ver ofertas</button>
          <div className="badge">
            <span>Hasta</span>
            <strong>[X]%</strong>
            <span>OFF</span>
          </div>
        </div>
      </header>
    </div>
  )
}

export default App