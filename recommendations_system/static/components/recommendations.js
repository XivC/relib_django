class Recommendations extends React.Component {



    render() {
        console.log(this.props.recommendations);
        var items = [];
        for (let book of this.props.recommendations) {
            items.push(<Book key={book.title} title={book.title} author={book.author} rubrics={book.rubric}/>)
        }

        return (
            <div>
                {items}
            </div>
        )
    }


}