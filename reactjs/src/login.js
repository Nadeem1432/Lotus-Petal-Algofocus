import React, { useState } from "react";
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import Input from '@mui/material/Input';
import FilledInput from '@mui/material/FilledInput';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import TextField from '@mui/material/TextField';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import { Button ,CircularProgress } from '@material-ui/core';
import logo from './assets/logo.png';
import * as Constants from './constants.js'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';

// for TextInput
// https://mui.com/components/text-fields/

export default class Login extends React.Component{

	state={
		email:"",
		password:"",
		showPassword:false,
		loading:false
	}

handleClickShowPassword=e=>{
	e.preventDefault();
    this.setState({showPassword: !this.state.showPassword})
  };

handleMouseDownPassword = (event) => {
    event.preventDefault();
  };


submitDataHandler = async(event,props) =>{
	event.preventDefault();
	await this.setState({loading:true})
	try{
		let response =	await axios.post(`${Constants.proxy_url}${Constants.base_url}api/v1/login/`,{
							username:this.state.email,
							password:this.state.password
						})
		await this.setState({loading:false})
		if(response.status==200 && response.data.user_data.user_type=="Admin"){
			await localStorage.setItem('token', response.data.token);
			await localStorage.setItem('user', response.data.user_data.user_email);

			await this.setState({loading:false})
			await this.props.history.push('/timetable')
//		alert("login succed")

		}else{
			await this.setState({loading:false})
		    await toast("Access Not allowed for Teachers... ")
			await toast(response.data.error_details)
		}

	}
	catch(error){
		await this.setState({loading:false})
		await toast("Invalid Credentials")
	}

  }



	render(){
		if(this.state.loading){
			return(
				<div style={{display:"flex",alignItems:"center",justifyContent:"center",position: 'absolute',top: 0, left: 0, right: 0, bottom: 0,}}>
						<CircularProgress color="#e0ffff" />
				</div>
			)
		}else{
		return(
		<div style={styles.boxStyle}>
			<ToastContainer />
			<div style={{}}>
								<img  src={logo} style={{width:"130px",height:"130px"}} />
			</div>
			<div>
				<FormControl sx={styles.textInputStyle} variant="outlined">
		          <InputLabel htmlFor="outlined-adornment-email">Email</InputLabel>
			          <OutlinedInput
			            id="outlined-adornment-email"
			            value={this.state.email}
			            onChange={(event)=>{this.setState({'email':event.target.value})}}
			            endAdornment={
			              <InputAdornment position="end">
			                <IconButton
			                  aria-label="toggle password visibility"
			                  edge="end"
			                >
		                </IconButton>
		              </InputAdornment>
		            }
		            label="Email"
		          />
		        </FormControl>
		        </div>

		        <div>
				<FormControl sx={styles.textInputStyle} variant="outlined">
		          <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
			          <OutlinedInput
			            id="outlined-adornment-password"
			            type={this.state.showPassword ? 'text' : 'password'}
			            value={this.state.password}
			            onChange={(event)=>{this.setState({'password':event.target.value})}}
			            endAdornment={
			              <InputAdornment position="end">
			                <IconButton
			                  aria-label="toggle password visibility"
			                  onClick={this.handleClickShowPassword}
			                  onMouseDown={this.handleMouseDownPassword}
			                  edge="end"
			                >
		                  {this.state.showPassword ? <VisibilityOff /> : <Visibility />}
		                </IconButton>
		              </InputAdornment>
		            }
		            label="Password"
		          />
		        </FormControl>
			</div>
			<div>
				<Button style={styles.buttonstyle} type="Submit" onClick={this.submitDataHandler}>
					Login
				</Button>
			</div>
		</div>
			)
		}
	}
}


const styles={
	boxStyle:{
	 display:'flex',
	 flexDirection:'column',
	 justifyContent:'center',
	 alignItems:'center',
	 position:'absolute',
	 top:0,
	 bottom:0,
	 left:0,
	 right:0,
	 marginLeft:'30%',
	 marginTop:'5%',
	 marginBottom:'15%',
	 width:'40%',
	 height:"80%",
	 backgroundColor:"#fadbd7",
	 boxShadow: "2px 11px 24.57px 2.43px rgba(1,1,1,.08)",
	 borderRadius:'5px'

	},
	textInputStyle:{
	 m: 2,
	 width: '40ch' ,
	 backgroundColor:'#fff',
	 boxShadow: "2px 11px 24.57px 2.43px rgba(1,1,1,.08)",
	},
	buttonstyle:{
		width:'40ch',
		color:'#02075d'
	}
}