import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from 'axios';
import logo from './assets/logo.png'
import { Button ,Select,MenuItem,InputLabel ,CircularProgress} from '@material-ui/core';
import * as Constants from './constants.js'
import styles from './styles/Table.Module.css'


// CSS Modules, react-datepicker-cssmodules.css
// import 'react-datepicker/dist/react-datepicker-cssmodules.css';

class Attendance extends React.Component{



  state ={
  		startDate:new Date(),
  		claas:[],
  		loading:true,
  		sections :[],
  		periods:[],
  		class:"",
  		section:"",
  		period:"",
  		resData:[],
  		email:'',
  		loadTheader:false,


  		}





componentDidMount(){
				this.fetachAllClassAndSections()
		}


fetachAllClassAndSections = async () =>{
				let email 	=		 await localStorage.getItem('user')
				try{
						if(email){
							let res 		=		 await axios.get(`${Constants.proxy_url}${Constants.base_url}api/v1/all_claas_section/`)
							await this.setState({claas:res.data})
							await this.setState({email:email})
							await this.setState({loading: false})
							}else{
								window.location.href='/'
							}
						}catch(error){
							window.location.href='/'
						}

		}

logoutUser = async(event,props) =>{
			event.preventDefault();
			await this.setState({loading:true})
			await localStorage.removeItem('user')
			await localStorage.removeItem('token')
			window.location.href='/'

		}

submitDataHandler = async(event,props) =>{
			event.preventDefault();
			this.setState({loading:true})
			var date = this.state.startDate.getFullYear() + "-" + (this.state.startDate.getMonth() + 1) + "-" + this.state.startDate.getDate()
			let res  =	await axios.post(`${Constants.proxy_url}${Constants.base_url}api/v1/get_offline_attendance/`,
						{
							"date":date,
							"time_table_id":this.state.period
						}
						)
			await this.setState({resData:res.data})
			await this.setState({loading:false})
			await this.setState({loadTheader:true})
		}

navigateToTimeTable = async(event,props) =>{
		event.preventDefault()
		window.location.href='/timetable'
}



handleClassChange = (event) => {
	       this.setState({class:event.currentTarget.id});
	       var arrayLength = this.state.claas.length;
					for (var i = 0; i < arrayLength; i++) {
						if(event.currentTarget.id==(this.state.claas[i].claas_id)){
							this.setState({sections:this.state.claas[i].sections})
						}
		}
	  };




handleSectionChange = async(event) => {
	this.setState({section:event.currentTarget.id})
	var id = event.currentTarget.id
	let res 		=    await axios.post(`${Constants.proxy_url}${Constants.base_url}api/v1/get_time_table/`,{
														"section_id":id
													})
	await this.setState({periods:res.data})
};


handlePeriodChange = async(event) => {
	this.setState({period:event.currentTarget.id})

}

attendanceMapHandler(){

	return this.state.resData.map((t,k)=>{
			if(k==2){
				var style = stylee.attendancestyle
			}else{
				var style = stylee.attendancestyle2
			}

			if(t.status=="p"){
				var status = "PRESENT"
				var color = "#229954"
			}else{
				var status = "ABSENT"
				var color = "#FF0000"
			}

			return(
				<div style={style}>
					<div style={{border:"solid",borderWidth:"1px",borderColor:"#fff",backgroundColor:"#eee",width:"33.3%",height:"40px",alignItems:"center",justifyContent:"center",flex:1}}>
						<p style={stylee.textStyle}>{t.sudent_id}</p>
					</div>
					<div style={{border:"solid",borderWidth:"1px",borderColor:"#fff",backgroundColor:"#eee",width:"33.3%",height:"40px",alignItems:"center",justifyContent:"center",flex:1}}>
						<p style={stylee.textStyle}>{t.name}</p>
					</div>
					<div style={{border:"solid",borderWidth:"1px",borderColor:"#fff",width:"33.3%",height:"40px",backgroundColor:color,alignItems:"center",justifyContent:"center",flex:1}}>
							<p style={stylee.textStyle1}>{status}</p>
					</div>
				</div>
			)
		}
	)

}

classMaphandler(){
  	return this.state.claas.map((t,k)=>
  		(
  			<MenuItem id={t.claas_id} value={t.claas_id} key={k} >{t.claas_name}</MenuItem>
  			)
  	)

  }


sectionMapHandler(){

  	return this.state.sections.map((t,k)=>
  		(
  			<MenuItem id={t.section_id} value={t.section_id} key={k} >{t.section_name}</MenuItem>
  			)
  	)

  }

periodMapHandler(){
	  	var days = { "0" :["monday 1","monday 2","monday 3","monday 4","monday 5","monday 6","monday 7"],
	  	"1" : ["tuesday 1","tuesday 2","tuesday 3","tuesday 4","tuesday 5","tuesday 6","tuesday 7"],
	  	"2" : ["wednesday 1","wednesday 2","wednesday 3","wednesday 4","wednesday 5","wednesday 6","wednesday 7"],
	  	"3" : ["thursday 1","thursday 2","thursday 3","thursday 4","thursday 5","thursday 6","thursday 7"],
	  	"4" : ["friday 1","friday 2","friday 3","friday 4","friday 5","friday 6","friday 7"],
	  	"5" : ["saturday 1","saturday 2","saturday 3","saturday 4","saturday 5","saturday 6","saturday 7"],
	  }

  	return this.state.periods.map((t,k)=>{
  			var day = days[t.day]
  			var periodNo = t.period_no -1
  			var period = day[periodNo]
  			var name = `Period - ${period} / Subject - ${t.subject}`
	  		return(
	  			<MenuItem id={t.id} value={t.id} key={k}>{name}</MenuItem>
	  			)
	  	}
  	)
  }








  render(){
  	if(this.state.loading){
			return(
				<div style={{display:"flex",alignItems:"center",justifyContent:"center",position: 'absolute',top: 0, left: 0, right: 0, bottom: 0,}}>
						<CircularProgress color="#e0ffff" />
				</div>
			)
	}else{
	  return (
			<div style={stylee.mainDivStyle}>
					<div style={stylee.headerStyle}>
								<img  src={logo} style={{width:"100px",height:"100px",margin:"20px"}} />
								<div style={{justifyContent:'flex-end',display:'flex',flexDirection:'column',marginRight:"5%",justifyContent:"space-between"}}>
										<p style={{color:"#1b387b"}}>{this.state.email}</p>
										<div style={{display:'flex',justifyContent:"space-between"}}>
											<Button className={styles.monthInput}
												style={{border:"solid 1px",color:"orange"}} onClick={this.navigateToTimeTable} >
														TIME TABLE
											</Button>
											<Button className={styles.monthInput}
												style={{border:"solid 1px",color:"red"}} onClick={this.logoutUser} >
														LOGOUT
											</Button>
										</div>
								</div>					
					</div>
					
					<div style={stylee.divStyle}>
						<div style = {{width:"700px",display:"flex",flexDirection:"row",alignItems:"center",justifyContent:"center",marginTop:"20px",resizemode:"contain"}}>
							<InputLabel id="label" style={stylee.inputLabelStyle}>CLASS</InputLabel>
									<Select
											     labelId="class"
											     id="class"
											     defaultValue="none"
											     value={this.state.class}
											     onChange={this.handleClassChange}
											     style={{width:"650px",backgroundColor:"#fff",borderStyle: "solid",borderWidth:"1px",resizemode:"contain"}}
											   >
											     <MenuItem id="none" value="none" disabled>
											       (Class )
											     </MenuItem>

											     {this.classMaphandler()}

										   </Select>
						</div>

						<div style = {{width:"700px",display:"flex",flexDirection:"row",alignItems:"center",justifyContent:"center",marginTop:"30px"}}>
										   <InputLabel id="label" style={stylee.inputLabelStyle}>SECTION</InputLabel>
										   <Select
											     labelId="section"
											     id="section"
											     defaultValue="none"
											     value={this.state.section}
											     onChange={this.handleSectionChange}
											     style={{width:"650px",backgroundColor:"#fff",borderStyle: "solid",borderWidth:"1px",}}
											   >
											     <MenuItem id="none" value="none" disabled>
											       (Section )
											     </MenuItem>

											     {this.sectionMapHandler()}

									   </Select>
						</div>



						<div style = {{width:"700px",display:"flex",flexDirection:"row",alignItems:"center",justifyContent:"center",marginTop:"30px"}}>
										   <InputLabel id="label" style={stylee.inputLabelStyle}>PERIOD</InputLabel>
										   <Select
											     labelId="period"
											     id="period"
											     defaultValue="none"
											     value={this.state.period}
											     onChange={this.handlePeriodChange}
											     style={{width:"650px",backgroundColor:"#fff",borderStyle: "solid",borderWidth:"1px",}}
											   >
											     <MenuItem id="none" value="none" disabled>
											       (Period )
											     </MenuItem>

											     {this.periodMapHandler()}

									   </Select>
						</div>


				<div style = {{width:"700px",display:"flex",flexDirection:"row",alignItems:"center",justifyContent:"center",marginTop:"30px"}}>
				 	<InputLabel id="label" style={stylee.inputLabelStyle}>DATE</InputLabel>
					    <DatePicker 
					    		selected={this.state.startDate} 
					    			onChange={(date) => {
					    					this.setState({startDate:date})
					    					}} 
										/>
				</div>



				<div style = {{width:"700px",display:"flex",flexDirection:"row",alignItems:"center",justifyContent:"center",marginTop:"30px",marginBottom:"30px",backgroundColor:"#02075d",border:"solid",borderWidth:"1px"}}>
						<Button type="Submit" onClick={this.submitDataHandler}
										style={{width:"100%",color:"#fff"}} value="Submit"> 
									Submit
						</Button>
				</div>


			</div>

			{this.state.loadTheader ?
			<div style={{marginTop:"50px"}}>

				<div style={stylee.attendancestyle}>
					<div style={{border:"solid",borderWidth:"1px",borderColor:"#fff",width:"33.3%",height:"40px",backgroundColor:"#02075d",alignItems:"center",justifyContent:"center",flex:1}}>
						<p style={stylee.textStyle1}>STUDENT ID</p>
					</div>
					<div style={{border:"solid",borderWidth:"1px",borderColor:"#fff",width:"33.3%",height:"40px",backgroundColor:"#02075d",alignItems:"center",justifyContent:"center",flex:1}}>
						<p style={stylee.textStyle1}>STUDENT NAME</p>
					</div>
					<div style={{border:"solid",borderWidth:"1px",borderColor:"#fff",width:"33.3%",height:"40px",backgroundColor:"#02075d",alignItems:"center",justifyContent:"center",flex:1}}>
							<p style={stylee.textStyle1}>ATTENDANCE</p>
					</div>
				</div>
				{this.attendanceMapHandler()}
			</div> : null }


		</div>
	  		);
		}
	}
};


const stylee={
	datePickerStyle:{
        width:"50px",
        marginLeft:"50px",
	},
	inputLabelStyle:{
		color:"#1b387b",
		marginRight:"20px",
		marginLeft:"30px",
	},
	headerStyle:{
		display:"flex",
		backgroundColor:"#fadbd7",
		alignItems:"center",
		justifyContent:"space-between",
		boxShadow: "2px 11px 24.57px 2.43px rgba(1,1,1,.08)"
	},
	divStyle:{
					display:"flex",
					flex:1,
					marginTop:"50px",
					marginRight:"15%",
					marginLeft:"15%",
					flexDirection:"column",
					justifyContent:"space-between",
					alignSelf:"center",
					borderWidth:"1px",
					alignItems:"center",
					backgroundColor:"#e0ffff",
					shadowColor: 'black',
					shadowOffset: { width: 0, height: 2 },
					shadowOpacity: .1,
					shadowRadius: 8,
					boxShadow: "2px 11px 24.57px 2.43px rgba(1,1,1,.08)",
					borderRadius:"10px"
					
				},
	mainDivStyle:{
		flex:1
	},
	attendancestyle:{

		height:"40px",
		display:"flex",
		alignItems:"center",
		justifyContent:"space-between",
		marginLeft:"15%",
		marginRight:"15%",
		boxShadow: "2px 11px 24.57px 2.43px rgba(1,1,1,.08)"
	},
	attendancestyle2:{

		height:"40px",
		display:"flex",
		alignItems:"center",
		justifyContent:"space-between",
		marginLeft:"15%",
		marginRight:"15%",
		boxShadow: "2px 11px 24.57px 2.43px rgba(1,1,1,.08)"
	},
	markerStyle:{
		height:"40px",
		width:"40px",
		display:"flex",
		alignItems:"center",
		justifyContent:"center",
		backgroundColor:"#5fdba7",
		boxShadow: "2px 11px 24.57px 2.43px rgba(1,1,1,.08)"
	},
	textStyle:{
		color:"black",
		fontSize:"17px"
	},
	textStyle1:{
		color:"#fff",
		fontSize:"17px"
	}
}


export default Attendance;