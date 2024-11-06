import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import AdminActions from './components/AdminActions';
import CustomerActions from './components/CustomerActions';


const App = () => {
    const [role, setRole] = useState(null);

    const handleLoginSuccess = (userRole) => {
        setRole(userRole);
    };

    const renderActions = () => {
        if (role === 'admin') {
            return <AdminActions />;
        } else if (role === 'customer') {
            return <CustomerActions />;
        }
        return <LoginForm onLoginSuccess={handleLoginSuccess} />;
    };

    return (
        <div class="divCenter">          
            {renderActions()}
        </div>
    );
};

export default App;