class History extends React.Component {



    render() {
        var items = [];
        for (var book of this.props.history) {
            items.push(<Book key={book.title} title={book.title} author={book.author} />)
        }

        return (
            <div>
                {items}
            </div>
        )
    }



}