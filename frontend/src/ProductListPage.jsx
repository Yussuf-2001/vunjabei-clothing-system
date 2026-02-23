import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from './api';

const ProductListPage = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const res = await api.get('products/');
                setProducts(res.data.results || res.data);
                setLoading(false);
            } catch (error) {
                console.error("Failed to fetch products", error);
                setLoading(false);
            }
        };
        fetchProducts();
    }, []);

    if (loading) return <div className="text-center p-5"><h2>Loading Products...</h2></div>;

    return (
        <div>
            <h2 className="mb-4">Our Products</h2>
            <div className="row g-4">
                {products.map(product => (
                    <div key={product.id} className="col-6 col-md-4 col-xl-3">
                        <div className="card h-100 product-card shadow-sm">
                            <div className="product-media">
                                <img 
                                    src={product.image || '/media/product_images/default-product.svg'} 
                                    className="product-image" 
                                    alt={product.name} 
                                />
                            </div>
                            <div className="card-body d-flex flex-column">
                                <h5 className="card-title text-truncate" title={product.name}>{product.name}</h5>
                                <p className="card-text text-muted">{product.category_name || 'General'}</p>
                                <div className="mt-auto">
                                    <p className="product-price">TSh {parseFloat(product.price).toLocaleString()}</p>
                                    <Link to={`/customer/products/${product.id}`} className="btn btn-primary w-100">
                                        View Details
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
                {products.length === 0 && (
                    <div className="col-12">
                        <p className="text-center text-muted">No products available at the moment.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ProductListPage;
