import logo from './logo.svg';
import './App.css';
import Header from './components/Header';
import MainContent from './components/MainContent';
import Footer from './components/Footer';

export default function App() {
  return (
    <div className='container'>
      <Header />
      <MainContent />
      <Footer />
    </div>
  );
}