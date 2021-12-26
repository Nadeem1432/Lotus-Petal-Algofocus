import React, { PureComponent, Fragment } from 'react';

class Test extends React.Component {
	  state = {
		  a : [1,2,3,'nadeem','ravinder','nsb']
		    };

	  dataMapHandler(){
		      return this.state.a.map((t,key) =>{
			            return(
					            <p key={key}>{t}</p>
					          )
			          })
		    }

	  render() {
		      const { options, value } = this.state;

		      return (
			            <div>
			              {this.dataMapHandler()}
			            </div>
			          );
		    }
}

export default Test;