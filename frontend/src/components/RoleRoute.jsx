import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

const RoleRoute = ({ user, requiredRole, children }) => {
  const location = useLocation();

  if (!user) {
    // If not logged in, redirect to login
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  const hasRole = (requiredRole === 'admin' && user.is_staff) || (requiredRole === 'customer' && !user.is_staff);

  if (!hasRole) {
    // If logged in but wrong role, redirect to their default dashboard
    const defaultRoute = user.is_staff ? '/admin' : '/customer';
    return <Navigate to={defaultRoute} replace />;
  }

  return children;
};

export default RoleRoute;