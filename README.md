# gw2_beetlerace_server

Websocket server to use with [gw2_speedometer](https://github.com/killer415tv/gw2_speedometer) and [gw2_beetlerace_overlay](https://github.com/Spruudel/gw2_beetlerace_overlay).

## Usage

Upon connection, expects an initial packet with the following fields:

| Field  | Description  | Values                     |
| ------ | ------------ | -------------------------- |
| type   | message type | `"init"`                   |
| client | client type  | `"speedometer"` \| `"map"` |
| room   | room ID      | any string                 |

Example:

```
{
    type: "init",
    client: "map",
    room: "test"
}
```

The server then listens to all incoming packets from that connection and broadcasts them to all clients of the other type in the same room.
For example, when receiving a message from a `map` in room `123`, this message will be broadcast to all `speedometer` clients in room `123`.
