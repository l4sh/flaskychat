<template>
  <div class="chat wrapper">
    <div class="chat messages">
      <div v-for="msg in messages">
        <p>{{ msg.text }}</p>

      </div>
    </div>
    <div class="chat messagebox">
      <form @submit.prevent="send(message)">
          <textarea
            class="chat input"
            type="text"
            v-model="message"
            @keydown="inputHandler"
            placeholder="Enter your message">
          </textarea>
      </form>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import VueSocketio from 'vue-socket.io'

Vue.use(
  VueSocketio,
  `${location.protocol}//${location.hostname}:5000`)// ${location.port}`)
export default {
  name: 'chat',
  data () {
    return {
      message: null,
      messages: [],
      room: null,
      nick: null
    }
  },
  methods: {

    /**
     * Send message socket event
     */
    send (message) {
      if (message) {
        if (!this.parseCommand(message)) {
          this.$socket.emit('message', { text: message })
        }
        this.message = ''
      }
    },

    /**
     * Handle messagebox input
     */
    inputHandler (e) {
      if (e.keyCode === 13 && !e.shiftKey) {
        e.preventDefault()
        this.send(e.target.value)
      }
    },

    /**
     * Check if message is a valid client command and run it
     * or pass it to the server.
     */
    parseCommand (message) {
      if (!message.startsWith('/')) {
        // It's a regular message
        return false
      }

      message = message.substring(1).split(' ')
      let command = message[0]  // Commands start with _
      let options = message.slice(1)

      if (command in this.clientCommands()) {
        this.clientCommands(command)(options)
        return true
      }
    },

    /**
     * Handle client side commands
     */
    clientCommands (command) {
      let vm = this
      let commandList = {

        /**
         * Set user nickname
         */
        nick (options) {
          if (options.length < 1 && !/^[a-z0-9_]+$/.test(options[0])) {
            vm.pushErrorMessage(
              'You must enter a valid nick.',
              'INVALID_NICK')
            return
          }
          let nick = options[0]
          vm.$socket.emit('nick', {nick: nick})
        },

        /**
         * Join a room
         */
        join (options) {
          if (options.length < 1 && !/^#[a-z0-9#_-]+$/.test(options[0])) {
            vm.pushErrorMessage(
              'You must enter a valid room name.',
              'INVALID_ROOM_NAME')
            return
          }
          let room = options[0]
          vm.$socket.emit('join', {room: room})
        }
      }

      return command ? commandList[command] : commandList
    },

    /**
     * Add an error message to the list of messages
     */
    pushErrorMessage (text, error) {
      this.messages.push({
        error: error,
        text: text
      })
    }
  },

  /**
   * Handle SocketIO events
   */
  sockets: {

    /**
     * Handle client connection
     */
    connect () {
      console.log('Connected to server')

      // Remove connection error message if found
      let lastMessage = this.messages[this.messages.length - 1]

      if (lastMessage &&
          (lastMessage.error &&
           lastMessage.error === 'CONNECT_ERROR')) {
        this.messages.pop()
      }

      // TODO: allow multiple rooms
      // Join general channel on connect
      // this.clientCommands('join')(['#general'])
    },

    /**
     * On connection error
     */
    connect_error () {
      // Set connection error message
      let lastMessage = this.messages[this.messages.length - 1]

      if (lastMessage &&
          (lastMessage.error &&
           lastMessage.error === 'CONNECT_ERROR')) {
        return
      }

      this.messages.push({
        error: 'CONNECT_ERROR',
        text: 'Connection error...'
      })
    },
    message (message) {
      this.messages.push(message)
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.chat {
  color: #333;
  border-radius: 5px;
  padding: 10px;
  font-size: 1em;
}

.wrapper {
  max-width: 600px;
  grid-template-columns: 20% auto;
  grid-template-areas:
    "messages"
    "messagebox";
  margin: 0 auto;
  height: 50vh;
}

.messages {
  grid-area: messages;
  text-align: left;
  height: 100%;
  border: solid 1px #b1b1b1;
}

.messagebox {
  margin-top: 10px;
  grid-area: messagebox;
  border: solid 1px #b1b1b1;
}

textarea:focus, input:focus{
  outline: none;
}

.messagebox .chat.input {
  padding: 0;
  width: 100%;
  border: none;
  resize: none;
}

.wrapper {
  background-color: #fff;
  color: #444;
}

</style>
