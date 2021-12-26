import logo from './logo.svg';
import './App.css';
import Table from './table.js'
import Attendance from './attendance.js'
import Test from './test.js'
import Login from './login.js'
import {BrowserRouter as Router,Switch ,Route,Link} from 'react-router-dom'

function App() {
	  return (
		      <div className="App">
		          <Router >
			        <Switch>
				        <Route exact path='/' component={Login} />
					    <Route exact path='/timetable' component={Table} />
						<Route exact path='/attendance' component={Attendance} />
					</Switch>
				</Router>
		    </div>
		    );
}

export default App;
