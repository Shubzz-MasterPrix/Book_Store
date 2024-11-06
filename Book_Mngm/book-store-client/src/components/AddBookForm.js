import React, { useState } from 'react';
import axios from 'axios';

const AddBookForm = () => {
  const [formData, setFormData] = useState({
    id: '',
    title: '',
    genre: '',
    quantity: '',
    author: '',
    publication: '',
    price: '',
  });

  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle input field changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate the form data
    const validationErrors = validateForm(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setLoading(true);
    try {
      // Assuming you have a backend API at this endpoint
      const response =  await axios.post('http://127.0.0.1:5000/api/books', formData);
      setSuccessMessage('Book added successfully!');
      setFormData({
        id: '',
        title: '',
        genre: '',
        quantity: '',
        author: '',
        publication: '',
        price: '',
      });
    } catch (error) {
      console.error('Error adding book:', error);
      setSuccessMessage('Failed to add book. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Validate the form input data
  const validateForm = (data) => {
    const errors = {};
    // if (!data.id || !/^\d{13}$/.test(data.id)) {
    //   errors.id = 'Invalid ISBN. Please enter a 13-digit ISBN.';
    // }
    if (!data.title) {
      errors.title = 'Title is required.';
    }
    if (!data.genre) {
      errors.genre = 'Genre is required.';
    }
    if (!data.quantity || isNaN(data.quantity) || data.quantity < 0) {
      errors.quantity = 'Quantity must be a valid positive number.';
    }
    if (!data.author) {
      errors.author = 'Author is required.';
    }
    if (!data.publication) {
      errors.publication = 'Publication is required.';
    }
    if (!data.price || isNaN(data.price) || data.price < 0) {
      errors.price = 'Price must be a valid positive number.';
    }
    return errors;
  };

  return (
    <div className="add-book-form">
      <br></br>
      <h6>Add a New Book</h6>

      {/* Success message */}
      {successMessage && <p className="success-message">{successMessage}</p>}

      <form onSubmit={handleSubmit}>
        {/* ISBN */}
        <div className="form-group row">
          <label className='col-sm-2 col-form-label'>ISBN:</label>
          <div className='col-sm-10'>
          <input 
            type="text"
            name="id"
            value={formData.id}
            onChange={handleChange}
            placeholder="13-digit ISBN"
          />
          </div>
          
          {errors.id && <p className="error">{errors.id}</p>}
        </div>

        {/* Title */}
        <div className="form-group row">
          <label className='col-sm-2 col-form-label'>Title</label>
          <div className='col-sm-10'>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Book Title"
          />
          </div>
          {errors.title && <p className="error">{errors.title}</p>}
        </div>

        {/* Genre */}
        <div className="form-group row">
          <label className='col-sm-2 col-form-label'>Genre</label>
          <div className='col-sm-10'>
          <select
            name="genre"
            value={formData.genre}
            onChange={handleChange}
          >
            <option value="">Select Genre</option>
            <option value="Fiction">Fiction</option>
            <option value="Non-Fiction">Non-Fiction</option>
            <option value="Mystery & Thriller">Mystery & Thriller</option>
            <option value="Fantasy">Fantasy</option>
            <option value="Science Fiction">Science Fiction</option>
            <option value="Romance">Romance</option>
            <option value="Historical Fiction">Historical Fiction</option>
            <option value="Biography & Memoir">Biography & Memoir</option>
            <option value="Self-Help">Self-Help</option>
            <option value="Graphic Novels & Comics">Graphic Novels & Comics</option>
            <option value="Poetry">Poetry</option>
            <option value="Children's">Children's</option>
            <option value="Classic Literature">Classic Literature</option>
            <option value="Science & Technology">Science & Technology</option>
            <option value="Health & Wellness">Health & Wellness</option>
            <option value="Cookbooks">Cookbooks</option>
            <option value="Art & Photography">Art & Photography</option>
            <option value="Spirituality & Religion">Spirituality & Religion</option>
            <option value="Crime">Crime</option>
          </select>
          </div>
          {errors.genre && <p className="error">{errors.genre}</p>}
        </div>

        {/* Quantity */}
        <div className="form-group row">
          <label className='col-sm-2 col-form-label'>Quantity</label>
          <div className='col-sm-10'>
          <input
            type="number"
            name="quantity"
            value={formData.quantity}
            onChange={handleChange}
            placeholder="Quantity"
          />
          </div>
          {errors.quantity && <p className="error">{errors.quantity}</p>}
        </div>

        {/* Author */}
        <div className="form-group row">
          <label className='col-sm-2 col-form-label'>Author</label>
          <div className='col-sm-10'>
          <input
            type="text"
            name="author"
            value={formData.author}
            onChange={handleChange}
            placeholder="Author"
          />
          </div>
          {errors.author && <p className="error">{errors.author}</p>}
        </div>

        {/* Publication */}
        <div className="form-group row">
          <label className='col-sm-2 col-form-label'>Publication</label>
          <div className='col-sm-10'>
          <input
            type="text"
            name="publication"
            value={formData.publication}
            onChange={handleChange}
            placeholder="Publication"
          />
          </div>
          {errors.publication && <p className="error">{errors.publication}</p>}
        </div>

        {/* Price */}
        <div className="form-group row">
          <label className='col-sm-2 col-form-label'>Price (₹)</label>
          <div className='col-sm-10'>
          <input
            type="number"
            name="price"
            value={formData.price}
            onChange={handleChange}
            placeholder="Price"
          />
          </div>
          {errors.price && <p className="error">{errors.price}</p>}
        </div>

        {/* Submit Button */}
        <div className="form-group row">
          <div className='col-sm-2'></div>
          <div className='col-sm-10'>
            <button type="submit" disabled={loading} className="btn btn-primary mb-2">
              {loading ? 'Adding...' : 'Add Book'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default AddBookForm;
