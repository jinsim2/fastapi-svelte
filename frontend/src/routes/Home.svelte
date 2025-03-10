<script>
  import fastapi from "../lib/api";
  import { link } from 'svelte-spa-router'

  let question_list = [];

  function get_question_list() {
    fastapi('get','/api/question/list',{}, (json) => {
      question_list = json
    }) 
  }
    
  get_question_list()
</script>

<div class="container my-3">
  <table class="table">
      <thead>
      <tr class="table-dark">
          <th>번호</th>
          <th>제목</th>
          <th>작성일시</th>
      </tr>
      </thead>
      <tbody>
      {#each question_list as question, i}
      <tr>
          <td>{i+1}</td>
          <td>
              <a use:link href="/detail/{question.id}">{question.subject}</a>
          </td>
          <td>{question.create_date}</td>
      </tr>
      {/each}
      </tbody>
  </table>
  <div class="d-flex justify-content-between">
    <a use:link href="/question-create" class="btn btn-primary">질문 등록하기</a>
    
    <div class="d-flex gap-2">
      <a use:link href="/chat-create" class="btn btn-primary">채팅방 만들기</a>
      <a use:link href="/real-time-chat" class="btn btn-success">실시간 채팅</a>
    </div>
  </div>
</div>