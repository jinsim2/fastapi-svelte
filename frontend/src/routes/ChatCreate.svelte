<script>
    import fastapi from "../lib/api";

    let userName = "";
    let roomName = "";
  
    async function connectChat() {
      if (!userName.trim()) {
        alert("참가자 이름을 입력하세요.");
        return;
      }
      if (!roomName.trim()) {
        alert("채팅방 이름을 입력하세요.");
        return;
      }

      // fastapi() 함수를 사용해 활성 채팅방 목록 조회
      fastapi(
        "get",
        "/api/rooms",
        {},
        (activeRooms) => {
          // activeRooms는 서버에서 반환한 활성 방 목록 (예: 배열)
          if (activeRooms.includes(roomName)) {
            alert(`채팅방 '${roomName}'은 이미 활성화되어 있습니다. 실시간 채팅 목록을 통해 참여하세요.`);
            return;
          } else {
            // 활성화되어 있지 않으면 새 창으로 채팅방 생성
            const url = window.location.origin + "/#/ws-chat?room=" + encodeURIComponent(roomName) + "&userName=" + encodeURIComponent(userName);
            window.open(url, "_blank", "width=500,height=600");
          }
        },
        (error) => {
          alert("활성 채팅방 정보를 가져오는데 실패했습니다. 나중에 다시 시도해 주세요.");
          console.error("Error:", error);
        }
      );
    }
</script>

<div class="container my-3">
    <h3>채팅방 만들기</h3>
    <div class="mb-3">
        <label for="userName" class="form-label">참가자 이름:</label>
        <input id="userName" type="text" bind:value={userName} class="form-control" placeholder="채팅방에 표시될 이름을 입력하세요" />
        <label for="roomName" class="form-label">채팅방 이름:</label>
        <input id="roomName" type="text" bind:value={roomName} class="form-control" placeholder="채팅방 이름을 입력하세요" />
    </div>
    <button class="btn btn-primary" on:click={connectChat}>웹소켓 연결</button>
</div>