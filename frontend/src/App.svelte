<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import QuestionCreate from "./routes/QuestionCreate.svelte"
  import ChatCreate from './routes/ChatCreate.svelte';
  import ChatRoom from './routes/ChatRoom.svelte';
  import RealTimeChat from './routes/RealTimeChat.svelte';

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail,
    '/question-create': QuestionCreate,
    '/chat-create' : ChatCreate,
    '/ws-chat' : ChatRoom,
    '/real-time-chat' : RealTimeChat
  }
</script>

<Router {routes}/>
