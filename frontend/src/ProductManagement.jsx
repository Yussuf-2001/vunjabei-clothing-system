﻿import React, { useEffect, useState } from 'react';
import api from './api';

const ProductForm = ({ product, onSave, onCancel }) => {
  const [formData, setFormData] = useState({ name: '', category: '', price: '', quantity: '' });
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const loadCategories = async () => {
      try {
        const res = await api.get('categories/');
        setCategories(res.data.results || res.data);
      } catch (error) {
        console.error('Failed to fetch categories', error);
      }
    };

    loadCategories();

    if (product) {
      setFormData({
        name: product.name,
        category: product.category?.id || product.category || '',
        price: product.price,
        quantity: product.quantity,
      });
      setImagePreview(product.image || null);
    } else {
      setFormData({ name: '', category: '', price: '', quantity: '' });
      setImageFile(null);
      setImagePreview(null);
    }
  }, [product]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setImageFile(file || null);
    if (file) {
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = new FormData();
    payload.append('name', formData.name);
    payload.append('category', formData.category);
    payload.append('price', formData.price);
    payload.append('quantity', formData.quantity);
    if (imageFile) {
      payload.append('image', imageFile);
    }
    onSave(payload);
  };

  return (
    <div className="modal show" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <form onSubmit={handleSubmit}>
            <div className="modal-header">
              <h5 className="modal-title">{product ? 'Edit Product' : 'Add New Product'}</h5>
              <button type="button" className="btn-close" onClick={onCancel}></button>
            </div>
            <div className="modal-body">
              <div className="mb-3">
                <label className="form-label">Product Name</label>
                <input type="text" name="name" value={formData.name} onChange={handleChange} className="form-control" required />
              </div>
              <div className="mb-3">
                <label className="form-label">Category</label>
                <select name="category" value={formData.category} onChange={handleChange} className="form-select">
                  <option value="">Select Category</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-3">
                <label className="form-label">Price (TSh)</label>
                <input type="number" step="0.01" name="price" value={formData.price} onChange={handleChange} className="form-control" required />
              </div>
              <div className="mb-3">
                <label className="form-label">Stock Quantity</label>
                <input type="number" name="quantity" value={formData.quantity} onChange={handleChange} className="form-control" required />
              </div>
              <div className="mb-3">
                <label className="form-label">Product Image</label>
                <input type="file" name="image" onChange={handleFileChange} className="form-control" />
                {imagePreview && (
                  <div className="mt-2">
                    <p className="text-muted small mb-1">Preview:</p>
                    <img src={imagePreview} alt="Preview" style={{ height: '100px', width: '100%', objectFit: 'contain', borderRadius: '5px', border: '1px solid #ddd', backgroundColor: '#f8fafc' }} />
                  </div>
                )}
              </div>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onCancel}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary">
                Save Product
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

const ProductManagement = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await api.get('products/');
      setProducts(res.data.results || res.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleDelete = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      await api.delete(`products/${productId}/`);
      fetchProducts();
    } catch (error) {
      console.error('Failed to delete product:', error);
      alert('Failed to delete product.');
    }
  };

  const handleSave = async (productData) => {
    const url = editingProduct ? `products/${editingProduct.id}/` : 'products/';
    const method = editingProduct ? 'put' : 'post';

    try {
      await api({ method, url, data: productData });
      setShowForm(false);
      setEditingProduct(null);
      fetchProducts();
    } catch (error) {
      console.error('Error saving product:', error.response?.data || error);
      const details = error.response?.data;
      const msg =
        (typeof details === 'string' && details) ||
        details?.detail ||
        details?.image?.[0] ||
        details?.category?.[0] ||
        details?.name?.[0] ||
        details?.price?.[0] ||
        details?.quantity?.[0] ||
        'Failed to save data.';
      alert(msg);
    }
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setShowForm(true);
  };

  const handleAddNew = () => {
    setEditingProduct(null);
    setShowForm(true);
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center p-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid p-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h4 className="fw-bold text-dark mb-0">Product Management</h4>
        <button className="btn btn-primary btn-sm shadow-sm" onClick={handleAddNew} style={{ borderRadius: '20px', padding: '8px 20px' }}>
          + Add New Product
        </button>
      </div>

      <div className="row g-4">
        {products.map((product) => (
          <div key={product.id} className="col-6 col-md-4 col-lg-3">
            <div className="card h-100 product-card">
              <div className="product-media">
                {product.image ? (
                  <img src={product.image} alt={product.name} className="product-image" />
                ) : (
                  <div className="d-flex align-items-center justify-content-center h-100 text-muted product-image-fallback">
                    <span>No image</span>
                  </div>
                )}
                <span className="position-absolute top-0 end-0 badge bg-dark m-1 opacity-75 rounded-pill" style={{ fontSize: '0.7rem' }}>
                  {product.category_name || 'General'}
                </span>
              </div>

              <div className="card-body p-2 d-flex flex-column">
                <h6 className="card-title fw-bold text-dark mb-1 text-truncate" title={product.name}>
                  {product.name}
                </h6>
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <small className={product.quantity < 10 ? 'text-danger fw-bold' : 'text-success fw-bold'} style={{ fontSize: '0.75rem' }}>
                    {product.quantity} left
                  </small>
                </div>

                <div className="mt-auto">
                  <h6 className="product-price mb-2" style={{ fontSize: '0.9rem' }}>
                    TSh {parseFloat(product.price).toLocaleString()}
                  </h6>
                  <div className="d-flex justify-content-end gap-2">
                    <button
                      className="btn btn-outline-primary btn-sm px-3"
                      onClick={() => handleEdit(product)}
                      title="Edit"
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-outline-danger btn-sm px-3"
                      onClick={() => handleDelete(product.id)}
                      title="Delete"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}

        {products.length === 0 && (
          <div className="col-12 text-center py-5">
            <h5 className="text-muted">No products found.</h5>
            <p className="text-muted">Click the button above to add your first product.</p>
          </div>
        )}
      </div>

      {showForm && <ProductForm product={editingProduct} onSave={handleSave} onCancel={() => setShowForm(false)} />}
    </div>
  );
};

export default ProductManagement;
