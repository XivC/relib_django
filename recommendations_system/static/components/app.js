class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {userId: 0, history: [], recommendations: []};
    this.handler = this.handler.bind(this)
    this.process = this.process.bind(this);
    this.showError = this.showError.bind(this);
  }



    handler(userId) {
      this.setState({userId: userId});
     
      getUserInfo(userId).then(this.process, this.showError);
      console.log(userId);
    }


    process(response) {
    if (typeof response.history !== 'undefined' && response.history.length > 0 && typeof response.recommendations !== 'undefined' && response.recommendations.length > 0 ){
        this.setState({history: response.history, recommendations: response.recommendations});
    }
    else {
      this.showError({statusText: "Такого пользователя не существует или нечего рекомендовать"});
    }
    }

    showError(error) {
     alert(error.statusText)
    }

  render() {
    return (<div>
      <Tabs>
        <div label={"Пользователь"}>
        <Profile setUserId={this.handler} userId={this.state.userId}/>
        </div>
        <div label="История">
          Ваша история:
          <History history={this.state.history}/>
        </div>
        <div label="Рекомендации">
          <Recommendations  recommendations={this.state.recommendations}/>
        </div>
      </Tabs>
    </div>);
  }
}



const domContainer = document.getElementById('container');
ReactDOM.render(<App />, domContainer);
