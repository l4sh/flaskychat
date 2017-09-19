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

Vue.use(VueSocketio, 'http://localhost:5000')

export default{
  name: 'chat',
  // el: '#container',
  data () {
    return {
      message: null,
      messages: []
    }
  },
  methods: {
    send (message) {
      if (message) {
        this.$socket.emit('message', { text: message })
        this.message = ''
      }
    },
    inputHandler (e) {
      if (e.keyCode === 13 && !e.shiftKey) {
        e.preventDefault()
        this.send(e.target.value)
      }
    }
  },
  sockets: {
    connect () {
      console.log('Connected to FlaskyChat server')

      // Remove connection error message if found
      let lastMessage = this.messages[this.messages.length - 1]

      if (lastMessage &&
          (lastMessage.error &&
           lastMessage.error === 'CONNECT_ERROR')) {
        this.messages.pop()
      }
    },
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
