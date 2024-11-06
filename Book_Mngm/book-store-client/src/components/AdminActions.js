import React, { useState } from 'react';
import AddBook from './AddBookForm';
import ViewSales from './ViewSales'
import ViewIncome from './ViewIncome'
import AdminViewBook from './AdminViewBook';

const AdminActions = () => {
    const [btnstate, setBtnState] = useState('View')
    const renderAdminPage = () => {
        if (btnstate === 'Add') {
            return <AddBook />;
        } else if (btnstate === 'Sales') {
            return <ViewSales />;
        }
        else if (btnstate === 'View') {
            return <AdminViewBook />;
        }
         else if (btnstate === 'Income') {
            return <ViewIncome />;
        }
        return <AddBook />;
    };
    return (
        <div>
            <div>
                <h4>Hello Admin.... </h4>
                <button onClick={() => setBtnState('View')}> View Books</button> &nbsp; &nbsp;
                <button onClick={() => setBtnState('Add')}> Add Books</button> &nbsp; &nbsp;
                <button onClick={() => setBtnState('Sales')}>View Sales</button> &nbsp; &nbsp;
                <button onClick={() => setBtnState('Income')}>View Total Income</button>
            </div>
            <div>
                {renderAdminPage()}
            </div>
        </div>
    );
};

export default AdminActions;
