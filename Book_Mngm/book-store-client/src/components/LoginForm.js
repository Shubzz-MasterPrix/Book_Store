import React, { useState } from 'react';
import axios from 'axios';

const LoginForm = ({ onLoginSuccess }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        
        e.preventDefault();
        setError('');

        try {

            const response = await axios.post('http://127.0.0.1:5000/api/login', {
                username: username,
                password: password
            });
            if (response.status === 200) {
                if (username == "admin") {
                    onLoginSuccess('admin');
                }
                else {
                    onLoginSuccess('customer');
                }

                    // Modify to differentiate roles
            }
           
           
        } catch (err) {
            
            	setError(err.response.data.error || 'Login failed');
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                &nbsp;
                <button type="submit" className="btn btn-primary mb-2">Login</button>
            </form>
        </div>
    );
};

export default LoginForm;