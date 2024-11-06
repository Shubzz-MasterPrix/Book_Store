import React, { useState, useEffect } from 'react';

const UserSearchBook = () => {
    const [books, setBooks] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterOption, setFilterOption] = useState('title'); // Default filter
    const [selectedBook, setSelectedBook] = useState(null);
    const [formData, setFormData] = useState({
        id: '',
        title: '',
        genre: '',
        quantity: '',
        author: '',
        publication: '',
        price: '',
      });

  // Handle row click to get selected book details
    const handleRowClick = (book) => {       
        setSelectedBook(book);        
    };

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
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({ ...prevData, [name]: value }));
      };

    return (
        <div>
            <h5>Book Search</h5>            
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
            <h5>Book List</h5>   
            <table class="table">
            <thead>
                <tr>
                    <th >Title</th>
                    <th>genre</th>
                    <th >author</th>
                    <th >publication</th>
                    <th >quantity</th>
                    <th >price</th>     
                    <th>Action</th>               
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
                        <td><button   onClick={() => handleRowClick(book)}>select to buy</button></td>
                     </tr>
                    
                ))}
                 </tbody>
            </table>
            {selectedBook && (
                <div style={{ marginTop: '20px' }}>
                    <h5>Selected Book Details</h5>
                    <p><strong>ISBN:</strong> {selectedBook.book_id}</p>
                    <p><strong>Title:</strong> {selectedBook.title}</p>
                    <p><strong>Author:</strong> {selectedBook.author}</p>
                    <p><strong>Price:</strong> {selectedBook.price}</p>
                    <p><strong>Genre:</strong> {selectedBook.genre}</p>
                    <div>
                    <input
                        type="number"
                        name="price"
                        value="1"
                        onChange={handleChange}
                        placeholder="Price"
                    />
                    </div>
                    &nbsp;
                    <div>
                    <button type="submit"  className="btn btn-primary mb-2">Buy Book </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UserSearchBook;