ticket_by_phone (phone)`{
    allEvents(phone:"{`+ phone + `") {
      edges {
        node {
          id
          phone
          ticket{
            id
            title
          }
        }
      }
    }
  }
`
  