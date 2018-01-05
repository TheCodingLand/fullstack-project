
def swagger():
    js = {
  "swagger": "2.0",
  "info": {
    "version": "0.0.1",
    "title": "Ot Service",
    "description": "Swagger spec for documenting the omnitracker service"
  },
  "host": "148.110.107.15:5001",
  "schemes": [
    "http"
  ],
  "securityDefinitions": {
    "Bearer": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header"
    }
  },
  "paths": {
    "/ping": {
      "get": {
        "description": "Returns a sanity check",
        "produces": [
          "application/json"
        ],
        "responses": {
          "200": {
            "description": "Will return 'pong!'"
          }
        }
      }
    },
     "/ot_objects/metadata/{id}": {
      "get": {
        "description": "Returns metadata from an object item",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of object to fetch",
            "required": True,
            "type": "integer",
            "format": "int64"
          }
        ],
        "responses": {
          "200": {
            "description": "metadata object"
          }
        }
      }
    },
     "/tickets/{id}": {
      "get": {
        "description": "Returns a ticket based on a single event ID",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of Ticket to fetch",
            "required": True,
            "type": "integer",
            "format": "int64"
          }
        ],
        "responses": {
          "200": {
            "description": "event object"
          }
        }
      }
    },
    "/events": {
      "get": {
        "description": "Returns all events",
        "produces": [
          "application/json"
        ],
        "responses": {
          "200": {
            "description": "event object"
          }
        }
      },
      "post": {
        "description": "Adds a new event",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "event",
            "in": "body",
            "description": "Event to add",
            "required": True,
            "schema": {
        
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Event added"
          }
        }
      }
    },
    "/events/{id}": {
      "get": {
        "description": "Returns an event based on a single event ID",
        "produces": [
          "application/json"
        ],
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "ID of Event to fetch",
            "required": True,
            "type": "integer",
            "format": "int64"
          }
        ],
        "responses": {
          "200": {
            "description": "event object"
          }
        }
      }
    },
  },
}
    return js  