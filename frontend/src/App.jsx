import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './Login';
import Register from './Register';
import PlaceOrder from './PlaceOrder';
import MyOrders from './MyOrders';

const ProductList = ({ user }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProducts = () => {
    axios.get('http://127.0.0.1:8000/api/products/')
      .then(response => {
        const data = Array.isArray(response.data) ? response.data : response.data.results;
        setProducts(data || []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching products:", err);
        setError("Failed to connect to server.");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const navigate = useNavigate();

  const handleBuy = async (product) => {
    if (!user) {
      alert("Please login to buy items.");
      return;
    }
    navigate(`/place-order/${product.id}`);
  };

  if (loading) return (
    <div className="text-center my-5">
      <div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div>
      <p className="mt-2">Loading products...</p>
    </div>
  );

  if (error) return <div className="alert alert-danger shadow-sm">{error}</div>;

  return (
    <div className="row">
      {products.length > 0 ? (
        products.map(product => (
          <div key={product.id} className="col-6 col-md-4 col-lg-3 mb-4">
            <div className="card h-100 shadow-sm border-0" style={{ transition: 'transform 0.2s' }}>
              <div className="position-relative">
                {product.image ? (
                  <img src={product.image} className="card-img-top" alt={product.name} style={{height: '180px', objectFit: 'cover'}} />
                ) : (
                  <div className="d-flex justify-content-center align-items-center bg-light text-secondary" style={{height: '180px'}}>
                    <span>No Image</span>
                  </div>
                )}
                <span className="badge position-absolute top-0 end-0 m-2 shadow-sm" style={{ backgroundColor: 'rgba(111, 66, 193, 0.9)', color: 'white' }}>{product.category_name || 'New'}</span>
              </div>
              <div className="card-body d-flex flex-column p-3">
                <h6 className="card-title fw-bold text-dark text-truncate" title={product.name}>{product.name}</h6>
                <h5 className="fw-bold mb-2" style={{ color: '#dc3545' }}>
                  TSh {parseFloat(product.price).toLocaleString()}
                </h5>
                <div className="d-flex justify-content-between align-items-center mb-3 small">
                   <span className="text-muted">Stock: {product.quantity}</span>
                   <span className={product.quantity > 0 ? "text-success fw-bold" : "text-danger fw-bold"}>{product.quantity > 0 ? 'In Stock' : 'Sold Out'}</span>
                </div>
                <button 
                  className="btn mt-auto w-100 shadow-sm fw-bold text-white"
                  style={{ backgroundColor: '#6f42c1' }}
                  onClick={() => handleBuy(product)}
                  disabled={product.quantity <= 0}
                >
                  {product.quantity > 0 ? 'Buy Now' : 'Out of Stock'}
                </button>
              </div>
            </div>
          </div>
        ))
      ) : (
        <div className="col-12"><div className="alert alert-info text-center">No products found.</div></div>
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
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error("User data corrupted, clearing:", error);
        localStorage.removeItem('user');
      }
    }
  }, []);

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  return (
    <Router>
      <div className="container mt-5">
        <nav className="navbar navbar-expand-lg navbar-dark mb-5 rounded px-4 shadow d-flex justify-content-between" style={{ backgroundColor: '#6f42c1' }}>
          <span className="navbar-brand mb-0 h1 fw-bold text-uppercase">Vunjabei Shop</span>
          
          <div>
            {user ? (
              <span className="text-white fw-bold">
                <Link to="/my-orders" className="btn btn-sm btn-light text-primary fw-bold me-3">My Orders</Link>
                Welcome, {user.username} 
                <button className="btn btn-sm btn-outline-light ms-3" onClick={handleLogout}>Logout</button>
              </span>
            ) : (
              <span className="text-white-50 small">Welcome Guest</span>
            )}
          </div>
        </nav>

        <Routes>
          <Route path="/login" element={user ? <Navigate to="/products" /> : <Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/products" element={user ? <ProductList user={user} /> : <Navigate to="/login" />} />
          <Route path="/place-order/:productId" element={user ? <PlaceOrder user={user} /> : <Navigate to="/login" />} />
          <Route path="/my-orders" element={user ? <MyOrders user={user} /> : <Navigate to="/login" />} />
          <Route path="/" element={<Navigate to={user ? "/products" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
