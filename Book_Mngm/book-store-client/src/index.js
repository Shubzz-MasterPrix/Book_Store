import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import imglogo from './book.png'
import 'bootstrap/dist/css/bootstrap.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div class="row grow w-100">
      <div class="col-12 bg-primary py-3 ">
      <h1 className='text-center'><span style={{color:'white'}}>Alpine Book store</span></h1>
      <p className='text-center'style={{color:'white'}}>A <b>complete</b>  store for all books.</p>
      </div>
      <div class="col-4 bg-info py-3">
      <img src={imglogo}  style={{height:"450px"}}/>
      </div>
      <div class="main col-8 bg-warning  py-3">
      <App />  
       </div>
    </div>
    <div class="row w-100">
      <div class="col-12 py-3 bg-danger">
      <h6 className='text-center' style={{ marginTop: "5px", color:'white' }}> Developed by (1) Devam Yogeshkumar Patel (2) Shubham Goel & (3) Yash Rastogi</h6>
  
      </div>
    </div>





  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
