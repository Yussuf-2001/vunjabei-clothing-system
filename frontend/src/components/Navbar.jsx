import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = ({ user, setUser }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
      <div className="container">
        <Link className="navbar-brand fw-bold text-danger" to={user ? (user.is_staff ? '/admin' : '/customer') : '/login'}>
          VUNJABEI
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          {user && (
            <ul className="navbar-nav me-auto">
              {user.is_staff ? (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" to="/admin">
                      Dashboard
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/admin/products">
                      Products
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/admin/orders">
                      Orders
                    </Link>
                  </li>
                </>
              ) : (
                <>
                  <li className="nav-item">
                    <Link className="nav-link" to="/customer/products">
                      Products
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/customer/my-orders">
                      My Orders
                    </Link>
                  </li>
                </>
              )}
            </ul>
          )}

          <ul className="navbar-nav ms-auto">
            {user ? (
              <li className="nav-item dropdown">
                <button
                  className="btn btn-link nav-link dropdown-toggle text-white text-decoration-none"
                  id="userMenu"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                  type="button"
                >
                  {user.username} {user.is_staff ? '(Admin)' : '(Customer)'}
                </button>
                <ul className="dropdown-menu dropdown-menu-end">
                  <li>
                    <button className="dropdown-item" onClick={handleLogout} type="button">
                      Logout
                    </button>
                  </li>
                </ul>
              </li>
            ) : (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/login">
                    Login
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="btn btn-danger ms-2" to="/register">
                    Register
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
