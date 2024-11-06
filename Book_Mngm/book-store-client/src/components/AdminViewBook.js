import React, { useState, useEffect } from 'react';

const AdminViewBook = () => {
    const [books, setBooks] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterOption, setFilterOption] = useState('title');
    useEffect(() => {
        // Simulate fetching data from an API or database
        const fetchBooks = async () => {
            const response = await fetch('http://127.0.0.1:5000/api/books'); // Adjust the API endpoint as needed
            const data = await response.json();
            setBooks(data);
        };
        fetchBooks();
    }, []);

    const handleSearch = () => {
      
        return books.filter(book => {
            const searchValue = book[filterOption].toLowerCase();
            return searchValue.includes(searchTerm.toLowerCase());
        });
    };
    return (
       
        <div>
            <br></br>
            <h6>View Book </h6>
            <div>
                <select onChange={(e) => setFilterOption(e.target.value)} value={filterOption}>
                    <option value="title">Title</option>
                    <option value="genre">Genre</option>
                    <option value="author">Author</option>
                    <option value="publication">Publication</option>
                </select> &nbsp;&nbsp;
                <input
                    type="text"
                    placeholder="Search..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                {/*<button onClick={handleSearch}>Search</button>*/}
            </div>
            <h6>Book List</h6>   
            <table class="table">
            <thead>
                <tr>
                    <th >Title</th>
                    <th>genre</th>
                    <th >author</th>
                    <th >publication</th>
                    <th >quantity</th>
                    <th >price</th>
                </tr>
                </thead>
                <tbody>
                {handleSearch().map(book => (
                    <tr id={book.book_id} >
                        <td >{book.title}</td>
                        <td >{book.genre}</td>
                        <td >{book.author}</td>
                        <td >{book.publication}</td>
                        <td >{book.quantity}</td>
                        <td >₹{book.price}</td>                       
                     </tr>
                    
                ))}
                 </tbody>
            </table>

        </div>
    );
};

export default AdminViewBook;
