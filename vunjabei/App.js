import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './Login';
import Register from './Register';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/products/')
      .then(response => {
        const data = Array.isArray(response.data) ? response.data : response.data.results;
        setProducts(data || []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching products:", err);
        setError("Imeshindwa kuunganisha na server.");
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div className="text-center my-5">
      <div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div>
      <p className="mt-2">Inapakia bidhaa...</p>
    </div>
  );

  if (error) return <div className="alert alert-danger shadow-sm">{error}</div>;

  return (
    <div className="row">
      {products.length > 0 ? (
        products.map(product => (
          <div key={product.id} className="col-md-4 mb-4">
            <div className="card h-100 shadow-sm border-0">
              {product.image ? (
                <img src={product.image} className="card-img-top" alt={product.name} style={{height: '250px', objectFit: 'cover'}} />
              ) : (
                <div className="d-flex justify-content-center align-items-center bg-light text-secondary" style={{height: '250px'}}>
                  <span>Hakuna Picha</span>
                </div>
              )}
              <div className="card-body d-flex flex-column">
                <h5 className="card-title">{product.name}</h5>
                <p className="card-text text-muted small">{product.category_name || 'Hakuna Kategoria'}</p>
                <h6 className="card-subtitle mb-3 text-warning fw-bold fs-5">
                  TSh {parseFloat(product.price).toLocaleString()}
                </h6>
                <p className="card-text small mb-3">Zimebaki: <span className="fw-bold">{product.quantity}</span></p>
                <button className="btn btn-light mt-auto w-100 shadow-sm">Nunua Sasa</button>
              </div>
            </div>
          </div>
        ))
      ) : (
        <div className="col-12"><div className="alert alert-info text-center">Hakuna bidhaa zilizopatikana.</div></div>
      )}
    </div>
  );
};

// --- MAIN APP COMPONENT ---

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  return (
    <Router>
      <div className="container mt-5">
        <nav className="navbar navbar-expand-lg navbar-warning bg-warning mb-4 rounded px-3 d-flex justify-content-between">
          <span className="navbar-brand mb-0 h1 fw-bold">Vunjabei Shop</span>
          
          <div>
            {user ? (
              <span className="fw-bold">
                Karibu, {user.username} 
                <button className="btn btn-sm btn-danger ms-2" onClick={handleLogout}>Logout</button>
              </span>
            ) : (
              <span className="text-muted small">Karibu Mteja</span>
            )}
          </div>
        </nav>

        <Routes>
          <Route path="/login" element={user ? <Navigate to="/products" /> : <Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/products" element={user ? <ProductList /> : <Navigate to="/login" />} />
          <Route path="/" element={<Navigate to={user ? "/products" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;