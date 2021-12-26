import React from 'react';
import { Button ,Select,MenuItem,InputLabel ,CircularProgress} from '@material-ui/core';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import section from './data.js'
import logo from './assets/logo.png'
import axios from 'axios'
import * as Constants from './constants.js'
import styles from './styles/Table.Module.css'
import moment from 'moment'
// import {BrowserRouter as Router,Switch,Route,Redirect,} from "react-router-dom";
// import { useNavigate } from "react-router-dom"

import { CSVLink } from "react-csv";




class Table extends React.Component{


state={
		csv_filename:"report.csv",
		csv_data:[],
		loading:true,
		startDate:new Date(),
		data:[],
		claas :[],
		sections :[],
		teachers :Constants.teachers,
		subjects :[{"id":1,"name":"first select class and section"}],
		class:"",
		section:"",
		subject:{monday:{},tuesday:{},wednesday:{},thursday:{},friday:{},saturday:{}},
		teacher:{monday:{},tuesday:{},wednesday:{},thursday:{},friday:{},saturday:{}},
		util1:{monday:{},tuesday:{},wednesday:{},thursday:{},friday:{},saturday:{}},
		weeks:[{'id':0,'name':"week 1"},{'id':1,'name':"week 2"},{'id':2,'name':"week 3"},{'id':3,'name':"week 4"},{'id':4,'name':"week 5"},{'id':5,'name':"week 6"}],
		week:"",
		weekData:[[],[],[],[],[]],
		days:[],
		weekDays:[],
		weekDaysSend:[],
		monthYear:"",
		totalSundays:"",
		monday:Constants.monday,
		tuesday:Constants.tuesday,
		wednesday:Constants.wednesday,
		thursday:Constants.thursday,
		friday:Constants.friday,
		saturday:Constants.saturday,
		abc:[{"id":1,"name":"first select class and section"}],
		postData:{
			"0":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"1":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"2":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"3":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"4":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"5":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}}
		},
		afterPostData:{
			"0":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"1":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"2":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"3":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"4":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}},
			"5":{"1":{},"2":{},"3":{},"4":{},"5":{},"6":{},"7":{}}
		},

	}



		componentDidMount(){
				this.fetachAllClassAndSections()
		}



		submitDataHandler = async(event,props) =>{
			event.preventDefault();
			try{
					var PostDataArray  		=			[]
					var data  	 =	this.state.postData
					for(var i=0;i<6;i++){
						var dict   =	 data[String(i)]
						for (const [key, value] of Object.entries(dict)){
							if(Object.keys(dict[key]).length===0){
								delete dict[key]
							}
						}	
					}
					for (const [key, value] of Object.entries(data)){
							if(Object.keys(data[key]).length===0){
								delete data[key]
							}
						}
					console.log(data)
					PostDataArray.push({"section_id":this.state.section})
					// PostDataArray.push({"week":this.state.week})
					// PostDataArray.push({"month":String(this.state.monthYear.getMonth()+1)})
					// PostDataArray.push({"year":String(this.state.monthYear.getFullYear())})
				  	PostDataArray.push({"days":data})
					console.log(JSON.stringify(PostDataArray))
					await axios.post(`${Constants.proxy_url}${Constants.base_url}api/v1/update_timetable/`,PostDataArray)
							.then(response=>
									{ 
										 alert(response.data.detail)
										 window.location.reload()
										// this.setState({postData:this.state.afterPostData})
									})
				}catch(err){
					console.log(err)
					alert("Nothing To Update....")
					// await this.setState({postData:this.state.afterPostData})
					window.location.reload()
				}
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




		handleClassChange = (event) => {
	       this.setState({class:event.currentTarget.id});
		   if(this.state.week!=="" && this.state.monthYear!==""){
				var arrayLength = this.state.claas.length;
							for (var i = 0; i < arrayLength; i++) {
								if(event.currentTarget.id==(this.state.claas[i].claas_id)){
									this.setState({sections:this.state.claas[i].sections})
								}
				}
			}
	  };


navigateAttendance = async(event,props) =>{
		event.preventDefault()
		window.location.href='/attendance'
}



handleWeekChange = async(event) =>{
	var id = parseInt(event.currentTarget.id)
	this.setState({week:event.currentTarget.id})
	if(this.state.monthYear!==""&& this.state.class!==""){
		var arrayLength = this.state.claas.length;
					for (var i = 0; i < arrayLength; i++) {
						if(this.state.class==(this.state.claas[i].claas_id)){
							this.setState({sections:this.state.claas[i].sections})
						}
		}
	}
	 await this.setState({ days: this.state.weekData[event.currentTarget.id] })
	 var dayData = [null,null,null,null,null,null]
	 var reDayData = [null,null,null,null,null,null]
	 var weekD = this.state.weekData[id]
	 for(let i =0;i<weekD.length;i++){
		 var day = this.state.days[i].getDay()
		 dayData[day-1] = moment(this.state.days[i]).format('DD-MM-YYYY')
		 reDayData[day-1] = moment(this.state.days[i]).format('YYYY-MM-DD')
	 }
	 await this.setState({weekDays:dayData})
	 await this.setState({weekDaysSend:reDayData})
	 await console.log(this.state.days)
	 await console.log(dayData)
}

dateMonthChangeHandler = async(date) =>{
			await this.setState({monthYear:date})
			if(this.state.week!==""&& this.state.class!==""){
				var arrayLength = this.state.claas.length;
							for (var i = 0; i < arrayLength; i++) {
								if(this.state.class==(this.state.claas[i].claas_id)){
									await this.setState({sections:this.state.claas[i].sections})
								}
				}
			}
			var days = await this.getDaysInMonth(date.getMonth(),date.getFullYear())
			await console.log(days)
			var sunBreak = [];
			var weekData = [[],[],[],[],[],[]]
			for(let i =0;i<days.length;i++){
				if(days[i].getDay()===0){
					await sunBreak.push(i)
				}
			}
			await console.log(sunBreak)
			for(let i =0;i < sunBreak.length+1 ; i++){
				if(i===0){
					for(let j =0;j<sunBreak[i];j++){
						weekData[i].push(days[j])
					}
					for(let j=sunBreak[i]+1;j<sunBreak[i+1];j++){
						weekData[i+1].push(days[j])
					}
				}
				if(i === (sunBreak.length -1)){
					for(let j = sunBreak[i]+1;j<days.length;j++){
						weekData[i+1].push(days[j])
					}
				}
				if(i !==0 &&i !==(sunBreak.length-1)){
					for (let j = sunBreak[i]+1;j<sunBreak[i+1];j++){
						weekData[i+1].push(days[j])
					}
				}
			}
			await this.setState({weekData:weekData})
			await console.log(this.state.weekData)
			await this.setState({totalSundays:sunBreak.length})
		}

getDaysInMonth = async(month, year) => {
			var date = new Date(year, month, 1);
			var days = [];
			while (date.getMonth() === month) {
			  await days.push(new Date(date));
			  await date.setDate(date.getDate() + 1);
			}
			return days;
		  }


handleSectionChange = async(event) => {

	  	 this.setState({loading:true})

	  	 var id = event.currentTarget.id
	     this.setState({subject:{monday:{},tuesday:{},wednesday:{},thursday:{},friday:{},saturday:{}},teacher:{monday:{},tuesday:{},wednesday:{},thursday:{},friday:{},saturday:{}}});
	     await this.setState({section:event.currentTarget.id});

				let res 		=    await axios.post(`${Constants.proxy_url}${Constants.base_url}api/v1/subject_teachers/`,{
														"section_id":id,
													})

				if(res.data.length!==0){
					await this.setState({subjects:res.data})
				}

				let res2 		=    await axios.post(`${Constants.proxy_url}${Constants.base_url}api/v1/get_time_table/`,{
														"section_id":id,
														"week":this.state.week+1,
														"month":this.state.monthYear.getMonth()+1,
														"year":this.state.monthYear.getFullYear()
													})

					if(res2.data.length!==0){
						var res_data  		=				await res2.data
						var week_name = this.state.week + 1
						this.setState({  csv_filename: `${this.state.monthYear.getFullYear()}-${this.state.monthYear.getMonth()+1}.csv`
						
						
						})
						this.setState({csv_data:res_data})
						
						var dayIndexArray =   ["monday","tuesday","wednesday","thursday","friday","saturday"]
						await Promise.all(res_data.map((key,value)=>{
							var day  			 		    						=   		  res_data[value].day
							var period_no  		    						=    		  res_data[value].period_no
							var day 			 		    						=				  dayIndexArray[parseInt(day)]
							var subject   										= 			  this.state.subject[day]
							subject[parseInt(period_no)]    	=         res_data[value].subject_id
							var teacher 											=				  this.state.teacher[day]
							teacher[parseInt(period_no)]			=				  res_data[value].teacher_id
							var name 													=				  day+" "+parseInt(period_no)
							var subjectsArray  								=				  res.data
							var length 												=				  res.data.length
							console.log(length)
							var subject_id        					  =         res_data[value].subject_id
						 Promise.all(subjectsArray.map((key,value)=>{
									if(subject_id==subjectsArray[value].subject_id){
										console.log(subjectsArray[value].subject_id)
										console.log(subject_id)
										console.log(value)
										this.state.teachers[name] =   subjectsArray[value].teachers
										this.state.abc =    subjectsArray[value].teachers
									  this.refreshHandler(name)
											}
										}	
									)
						 		)
							}
						)
					)
				}else{
					this.setState({subject:this.state.util1,teacher:this.state.util1})
				}
		  await this.setState({loading:false})
			
	  };


	  time_table_fetch_handler(){

	  }



	  handleSubjectChange =  (event,value) => {
	  		this.setState({loading:true})
	  	  var name 		=		 event.target.name.split(" ")[0]
	  	  var num 		=	   event.target.name.split(" ")[1]
	  	  var dayIndexArray =   ["monday","tuesday","wednesday","thursday","friday","saturday"]
	  	  var state   =    this.state[name]
	  	  var index   =	   String(dayIndexArray.indexOf(name))
	  	  var  arr    =    state[index]
	  	  var postDict  				=					this.state.postData
	  	  var dayData  					=					postDict[index]
	  	  var queryDict 				=					dayData[num]
	  	  queryDict["subject_id"] = 			event.target.value
	  	  queryDict["subject"] 		=				event.currentTarget.id
	  	  queryDict["is_online"]  =				1
		  queryDict["week"]  =				this.state.week +1
		  queryDict["month"]  =				this.state.monthYear.getMonth()+1
		  queryDict["year"]  =				this.state.monthYear.getFullYear()
		  queryDict["timetable_date"] =     this.state.weekDaysSend[dayIndexArray.indexOf(name)]
	  	  for (var i = 0; i < arr.length; i++) {
						if(num in arr[i]){
							var period 						=				 arr[i]
							var details						= 			 period[num]
							details["subject_id"] = 			 event.target.value
							details["subject"]    = 			 event.currentTarget.id
							var day   						= 			 this.state.subject[name]
							day[num]    					=         event.target.value
							var subjectsArray  		=				  this.state.subjects
							var subject_id        =         event.target.value
							for(var i=0; i < subjectsArray.length;i++){
								if(subject_id==subjectsArray[i].subject_id){
									this.state.teachers[event.target.name] =  subjectsArray[i].teachers
									this.state.abc =   subjectsArray[i].teachers
									 this.refreshHandler(event.target.name)
									 this.setState({loading:false})
								}
							}
						}
					} 
	  };

	  async refreshHandler(day){
	  	console.log(day)
	  	await this.teachersMapHandler(day)
	  }

	  handleTeacherChange = (event,value) => {
	  		this.setState({loading:true})
	  	  var name 		=		event.target.name.split(" ")[0]
	  	  var num 		=	  event.target.name.split(" ")[1]
	  	  var dayIndexArray =   ["monday","tuesday","wednesday","thursday","friday","saturday"]
	  	  var state   =   this.state[name]
	  	  var index   =	  String(dayIndexArray.indexOf(name))
	  	  var  arr    =   state[index]
	  	  var postDict  				=					this.state.postData
	  	  var dayData  					=					postDict[index]
	  	  var queryDict 				=					dayData[num]
	  	  queryDict["teacher_id"] = 			event.target.value
	  	  queryDict["teacher"] 		=				event.currentTarget.id
	  	  console.log(queryDict)
	  	  for (var i = 0; i < arr.length; i++) {
						if(num in arr[i]){
							var period 	=	arr[i]
							var details	= period[num]
							details["teacher_id"] = 			event.target.value
							details["teacher"]    = 			event.currentTarget.id
							var day   						= 			this.state.teacher[name]
							day[num]    					=        event.target.value
							console.log(this.state.monday)
							console.log(this.state.teacher)
							this.setState({loading:false})
						}
					} 
	  };




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

subjectsMapHandler(){

  	return this.state.subjects.slice(0).reverse().map((t,k)=>
  		{
  			return(
  			<MenuItem id={t.subject_name} value={t.subject_id} key={k}>{t.subject_name}</MenuItem>
  			)
  			}
  	)

  }

teachersMapHandler(day){
		var query 		=			this.state.teachers[day]
  	return query.map((t,k)=>
  		{
  			
  			return(
  				<MenuItem id={t.name} key={k} value={t.id} >{t.name}</MenuItem>
  				)
  			}
  	)

  }

weeksMapHandler(day){
	var query 		=			this.state.weeks
  return query.map((t,k)=>
	  {
		  
		  return(
			  <MenuItem id={t.id} key={k} value={t.id} >{t.name}</MenuItem>
			  )
		  }
  )

}

mondayMapHandler(){
  	var mon = ["monday 1","monday 2","monday 3","monday 4","monday 5","monday 6","monday 7"]
  	return mon.map((t,key)=>
  			{

  				var day 		= 	mon[key]
  				var period	= 	String(key+1)
  				var state   =		this.state.subject.monday[period]
  				var state2  =		this.state.teacher.monday[period]
  				return(

  				<div style={stylee.tableStyle} key={key}>
								<Select
											className={styles.monthInput}
										     labelId="subject"
										     id="subject"
										     name={day}
										     defaultValue="none"
										     value={state}
										     onChange={this.handleSubjectChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       SUBJECT
										     </MenuItem>

										     {this.subjectsMapHandler()}

									   </Select>
									<Select
											className={styles.monthInput}
										     labelId="teacher"
										     id="teacher"
										     name={day}
										     defaultValue="none"
										     value={state2}
										     onChange={this.handleTeacherChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       TEACHER
										     </MenuItem>

										     {this.teachersMapHandler(day)}

									   </Select>
							</div>

  				)
  			}

  	)
  }



tuesdayMapHandler(){
  	var tue = ["tuesday 1","tuesday 2","tuesday 3","tuesday 4","tuesday 5","tuesday 6","tuesday 7"]
  	return tue.map((t,key)=>
  			{

  				var day 		= 	tue[key]
  				var period	= 	String(key+1)
  				var state   =		this.state.subject.tuesday[period]
  				var state2  =		this.state.teacher.tuesday[period]
  				return(

  				<div style={stylee.tableStyle}>
								<Select
											className={styles.monthInput}
										     labelId="subject"
										     id="subject"
										     name={day}
										     defaultValue="none"
										     value={state}
										     onChange={this.handleSubjectChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       SUBJECT
										     </MenuItem>

										     {this.subjectsMapHandler()}

									   </Select>
									<Select
											className={styles.monthInput}
										     labelId="teacher"
										     id="teacher"
										     name={day}
										     defaultValue="none"
										     value={state2}
										     onChange={this.handleTeacherChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       TEACHER
										     </MenuItem>

										     {this.teachersMapHandler(day)}

									   </Select>
							</div>

  				)
  			}

  	)
  }

wednesdayMapHandler(){
  	var wed = ["wednesday 1","wednesday 2","wednesday 3","wednesday 4","wednesday 5","wednesday 6","wednesday 7"]
  	return wed.map((t,key)=>
  			{

  				var day 		= 	wed[key]
  				var period	= 	String(key+1)
  				var state   =		this.state.subject.wednesday[period]
  				var state2  =		this.state.teacher.wednesday[period]
  				return(

  				<div style={stylee.tableStyle}>
								<Select
											className={styles.monthInput}
										     labelId="subject"
										     id="subject"
										     name={day}
										     defaultValue="none"
										     value={state}
										     onChange={this.handleSubjectChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       SUBJECT
										     </MenuItem>

										     {this.subjectsMapHandler()}

									   </Select>
									<Select
											className={styles.monthInput}
										     labelId="teacher"
										     id="teacher"
										     name={day}
										     defaultValue="none"
										     value={state2}
										     onChange={this.handleTeacherChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       TEACHER
										     </MenuItem>

										     {this.teachersMapHandler(day)}

									   </Select>
							</div>

  				)
  			}

  	)
  }


thursdayMapHandler(){
  	var thur = ["thursday 1","thursday 2","thursday 3","thursday 4","thursday 5","thursday 6","thursday 7"]
  	return thur.map((t,key)=>
  			{

  				var day 		= 	thur[key]
  				var period	= 	String(key+1)
  				var state   =		this.state.subject.thursday[period]
  				var state2  =		this.state.teacher.thursday[period]
  				return(

  				<div className={styles.monthInput}
				  	style={stylee.tableStyle}>
								<Select
											className={styles.monthInput}
										     labelId="subject"
										     id="subject"
										     name={day}
										     defaultValue="none"
										     value={state}
										     onChange={this.handleSubjectChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       SUBJECT
										     </MenuItem>

										     {this.subjectsMapHandler()}

									   </Select>
									<Select
											className={styles.monthInput}
										     labelId="teacher"
										     id="teacher"
										     name={day}
										     defaultValue="none"
										     value={state2}
										     onChange={this.handleTeacherChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       TEACHER
										     </MenuItem>

										     {this.teachersMapHandler(day)}

									   </Select>
							</div>

  				)
  			}

  	)
  }


friayMapHandler(){
  	var fri = ["friday 1","friday 2","friday 3","friday 4","friday 5","friday 6","friday 7"]
  	return fri.map((t,key)=>
  			{

  				var day 		= 	fri[key]
  				var period	= 	String(key+1)
  				var state   =		this.state.subject.friday[period]
  				var state2  =		this.state.teacher.friday[period]
  				return(

  				<div style={stylee.tableStyle}>
								<Select
											className={styles.monthInput}
										     labelId="subject"
										     id="subject"
										     name={day}
										     defaultValue="none"
										     value={state}
										     onChange={this.handleSubjectChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       SUBJECT
										     </MenuItem>

										     {this.subjectsMapHandler()}

									   </Select>
									<Select
											className={styles.monthInput}
										     labelId="teacher"
										     id="teacher"
										     name={day}
										     defaultValue="none"
										     value={state2}
										     onChange={this.handleTeacherChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       TEACHER
										     </MenuItem>

										     {this.teachersMapHandler(day)}

									   </Select>
							</div>

  				)
  			}

  	)
  }


saturdayMapHandler(){
  	var sat = ["saturday 1","saturday 2","saturday 3","saturday 4","saturday 5","saturday 6","saturday 7"]
  	return sat.map((t,key)=>
  			{
				
  				var day 		= 	sat[key]
  				var period	= 	String(key+1)
  				var state   =		this.state.subject.saturday[period]
  				var state2  =		this.state.teacher.saturday[period]
  				return(

  				<div style={stylee.tableStyle}>
								<Select
											className={styles.monthInput}
										     labelId="subject"
										     id="subject"
										     name={day}
										     defaultValue="none"
										     value={state}
										     onChange={this.handleSubjectChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       SUBJECT
										     </MenuItem>

										     {this.subjectsMapHandler()}

									   </Select>
									<Select
											className={styles.monthInput}
										     labelId="teacher"
										     id="teacher"
										     name={day}
										     defaultValue="none"
										     value={state2}
										     onChange={this.handleTeacherChange}
										     style={stylee.dropStyle}
										   >
										     <MenuItem id="none" value="none" disabled>
										       TEACHER
										     </MenuItem>

										     {this.teachersMapHandler(day)}

									   </Select>
							</div>

  				)
  			}

  	)
  }


	render(){
		var csvReport ={
			filename:this.state.csv_filename,
			data:this.state.csv_data
		}
		var state = this.state
		var day   = this.state.days
		if(this.state.totalSundays===5){
			var renArray = [1,2,3,4]
		}else{
			var renArray = [1,2,3]
		}
		if(this.state.loading){
			return(
				<div style={{display:"flex",alignItems:"center",justifyContent:"center",position: 'absolute',top: 0, left: 0, right: 0, bottom: 0,}}>
						<CircularProgress />
				</div>
			)
		}else{
		return(
			<div>
					<div className={styles.monthInput} style={stylee.headerStyle}>
								<img  src={logo} style={{width:"100px",height:"100px",margin:"20px"}} />
								<div style = {{width:"200px",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center"}}>
									<InputLabel id="label" style={{color:"#1b387b",marginTop:"10px"}}>CLASS</InputLabel>
											<Select
														labelId="class"
														id="class"
														defaultValue="none"
														value={this.state.class}
														onChange={this.handleClassChange}
														className={styles.monthInput}
														style={{width:"150px",backgroundColor:"#fff",marginTop:"10px"}}
													>
														<MenuItem id="none" value="none" disabled>
															CLASS
														</MenuItem>

														{this.classMaphandler()}

												</Select>
								</div>
								<div style = {{marginLeft:"10px",width:"200px",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center"}}>
										<InputLabel id="label" style={{color:"#1b387b",marginTop:"10px"}}>MONTH/YEAR</InputLabel>
													<DatePicker
														className={styles.monthInput}
														selected={this.state.monthYear}
														onChange={this.dateMonthChangeHandler}
														dateFormat="MM/yyyy"
														style={{width:"150px",backgroundColor:"#fff",marginTop:"10px"}}
														showMonthYearPicker
													/>
													        {/* <Datepicker
																controls={['calendar']}
																select="preset-range"
																firstSelectDay={1}
																selectSize={7}
															/> */}
								</div>
								<div style = {{width:"200px",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center"}}>
										   <InputLabel id="label" style={{color:"#1b387b",marginTop:"10px",marginLeft:"30px"}}>WEEK</InputLabel>
										   <Select
										   		className={styles.monthInput}
											     labelId="Week"
											     id="Week"
											     defaultValue="none"
											     value={this.state.week}
											     onChange={this.handleWeekChange}
											     style={{width:"150px",backgroundColor:"#fff",marginTop:"10px"}}
											   >
											     <MenuItem id="none" value="none" disabled>
											       WEEK
											     </MenuItem>

											     {this.weeksMapHandler()}

									   </Select>
								</div>
								<div style = {{width:"200px",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center"}}>
										   <InputLabel id="label" style={{color:"#1b387b",marginTop:"10px",marginLeft:"30px"}}>SECTION</InputLabel>
										   <Select
										   		className={styles.monthInput}
											     labelId="section"
											     id="section"
											     defaultValue="none"
											     value={this.state.section}
											     onChange={this.handleSectionChange}
											     style={{width:"150px",backgroundColor:"#fff",marginTop:"10px"}}
											   >
											     <MenuItem id="none" value="none" disabled>
											       SECTION
											     </MenuItem>

											     {this.sectionMapHandler()}

									   </Select>
								</div>
								<div style={{justifyContent:'flex-end',display:'flex',flexDirection:'column',marginRight:"5%"}}>
			<p style={{color:"#1b387b"}}><CSVLink {...csvReport}>Export</CSVLink>
</p>						
			<p style={{color:"#1b387b"}}>{this.state.email}</p>
									<div style={{display:'flex',justifyContent:"space-between"}}>
											<Button className={styles.monthInput}
												style={{color:"orange",border:'solid 1px'}} onClick={this.navigateAttendance} >
														ATTENDANCE
											</Button>
											<Button className={styles.monthInput}
												style={{color:"red",border:'solid 1px'}} onClick={this.logoutUser} >
														LOGOUT
											</Button>
									</div>
								</div>
					</div>
			<div style={{display:"flex",flexDirection:"row",justifyContent:"center",marginTop:"100px",elevation:"10px"}}>
						<div style={stylee.tableStyle1}>
							<p></p>
						</div>
						<div style={stylee.tableStyle1}>
							<p style={stylee.textStyle}>Period 1</p>
							<p style={stylee.textStyle}>8:30 AM to 9:20AM</p>
						</div>
						<div style={stylee.tableStyle1}>
							<p>Period 2</p>
							<p>9:20AM to 10:10AM</p>
						</div>
						<div style={stylee.tableStyle1}>
							<p>Period 3</p>
							<p>10:10 AM to 11:00AM</p>
						</div>
						<div style={stylee.tableStyle1}>
							<p>Period 4</p>
							<p>11:00 AM to 12:00PM</p>
						</div>
						<div style={stylee.tableStyle1}>
							<p>Period 5</p>
							<p>01:00 PM to 01:50PM</p>
						</div>
						<div style={stylee.tableStyle1}>
							<p>Period 6</p>
							<p>01:50 PM to 02:40PM</p>
						</div>
						<div style={stylee.tableStyle1}>
							<p>Period 7</p>
							<p>02:40 PM to 03:30PM</p>
						</div>
			</div>
			{((state.days.length >5 && state.week==0) || (state.days.length >0 && parseInt(state.week)===parseInt(state.totalSundays)) || (renArray.includes(parseInt(state.week))))?
			<div style={{display:"flex",flexDirection:"row",justifyContent:"center",elevation:"10px"}}>
						<div style={stylee.tableStyle}>
							<p>Monday</p>
							<p>{this.state.weekDays[0]}</p>
						</div>
						 {this.mondayMapHandler()}
			</div>
			: null}
			{((state.days.length >4 && state.week==0 )|| (state.days.length >1 &&  parseInt(state.week)===parseInt(state.totalSundays)) ||  (renArray.includes(parseInt(state.week)))) ?			
			<div style={{display:"flex",flexDirection:"row",justifyContent:"center",elevation:"10px"}}>
						<div style={stylee.tableStyle}>
							<p>Tuesday</p>
							<p>{this.state.weekDays[1]}</p>
						</div>
						{this.tuesdayMapHandler()}
			</div>
			: null}
			{((state.days.length >3 && state.week==0) || (state.days.length >2 &&  parseInt(state.week)===parseInt(state.totalSundays)) ||  (renArray.includes(parseInt(state.week)))) ?
			<div style={{display:"flex",flexDirection:"row",justifyContent:"center",elevation:"10px"}}>
						<div style={stylee.tableStyle}>
							<p>Wednesday</p>
							<p>{this.state.weekDays[2]}</p>
						</div>
						{this.wednesdayMapHandler()}		
			</div>
			: null}
			{((state.days.length >2 && state.week==0 )|| (state.days.length >3 &&  parseInt(state.week)===parseInt(state.totalSundays)) ||  (renArray.includes(parseInt(state.week)))) ?
			<div style={{display:"flex",flexDirection:"row",justifyContent:"center",elevation:"10px"}}>
						<div style={stylee.tableStyle}>
							<p>Thursday</p>
							<p>{this.state.weekDays[3]}</p>
						</div>
						{this.thursdayMapHandler()}
			</div>
			: null}
			{((state.days.length >1 && state.week==0) || (state.days.length >4 &&  parseInt(state.week)===parseInt(state.totalSundays)) ||  (renArray.includes(parseInt(state.week)))) ?
			<div style={{display:"flex",flexDirection:"row",justifyContent:"center",elevation:"10px"}}>
						<div style={stylee.tableStyle}>
							<p>Friday</p>
							<p>{this.state.weekDays[4]}</p>
						</div>
						{this.friayMapHandler()}		
			</div>
			: null}
			{((state.days.length >0 && state.week==0) || (state.days.length >5 &&  parseInt(state.week)===parseInt(state.totalSundays)) ||  (renArray.includes(parseInt(state.week)))) ?
			<div style={{display:"flex",flexDirection:"row",justifyContent:"center",elevation:"10px"}}>
						<div style={stylee.tableStyle}>
							<p>Saturday</p>
							<p>{this.state.weekDays[5]}</p>
						</div>
						{this.saturdayMapHandler()}
			</div>
			: null}
			<div className={styles.monthInput}
				style={stylee.buttonDivStyle}>
				<Button type="Submit" onClick={this.submitDataHandler}
								style={{width:"100%",color:"#289b2e"}} value="Submit"> 
							Submit
				</Button>
			</div>


			</div>

			)

		}

	}
}


const stylee ={
			headerStyle:{
				display:"flex",
				backgroundColor:"#fadbd7",
				display:"flex",
				alignItems:"center",
				justifyContent:"space-between",
				boxShadow: "2px 11px 24.57px 2.43px rgba(1,1,1,.08)"
			},
			textStyle:{
			},
			divStyle:{
					display:"flex",
					alignItems:"center",
					marginTop:"50px",
					marginLeft:"50px"
				},
			tableStyle:{
				width:"200px",
				height:"100px",
				backgroundColor:"#e0ffff",
				borderStyle: "solid",
				borderWidth:"1px",
				display:"flex",
				flex:1,
				alignItems:"center",
				justifyContent:"center",
				flexDirection:"column"
			},
			tableStyle1:{
				width:"200px",
				height:"100px",
				backgroundColor:"#e0ffff",
				borderStyle: "solid",
				borderWidth:"1px",
				display:"flex",
				justifyContent:"center",
				alignItems:"center",
				flexDirection:"column"
			},
			dropStyle:{
				width:"150px",
			  backgroundColor:"#fff",
			  margin:"5px"
			},
			buttonDivStyle:{
				border:"solid",
				marginTop:"100px",
				borderColor:"#289b2e",
				borderWidth:"1px",
				marginBottom:"100px",
				width:"80%",
				alignItems:"center",
				justifyContent:"center",
				marginLeft:"10%"}
}


export default Table;
