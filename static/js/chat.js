const joinOrLeave = document.querySelector("#join-leave");
const shareScreenButton = document.querySelector("#share-screen");
const callContainer = document.querySelector("#call-container");
const count = document.getElementById("count");
let connected = false;
let room;
let screenTrack;

const addLocalVideo = () => {
  Twilio.Video.createLocalVideoTrack().then((track) => {
    let video = document.querySelector("#local");
    let trackElement = track.attach();

    trackElement.addEventListener("click", () => {
      zoomTrack(trackElement);
    });
    video.appendChild(trackElement);
  });
};

const connectButtonHandler = (event) => {
  event.preventDefault();

  if (!connected) {
    let username = document.querySelector("#token").innerHTML;

    joinOrLeave.disabled = true;
    joinOrLeave.innerHTML = "Connecting...";
    connect(username);
  } else {
    disconnect();
    joinOrLeave.innerHTML = "Join call";
    connected = false;
    shareScreenButton.innerHTML = "Share screen";
    shareScreenButton.disabled = true;
  }
};

const connect = (username) => {
  Twilio.Video.connect(document.querySelector("#token").innerHTML)
    .then((_room) => {
      room = _room;

      room.participants.forEach(participantConnected);
      room.on("participantConnected", participantConnected);
      room.on("participantDisconnected", participantDisconnected);
      connected = true;
      joinOrLeave.innerHTML = "Leave call";
      joinOrLeave.disabled = false;
      shareScreenButton.disabled = false;
      updateParticipantCount();
    })
    .catch(() => {
      alert("Connection failed. Is the backend running?");
      joinOrLeave.innerHTML = "Join call";
      joinOrLeave.disabled = false;
    });
};

const participantConnected = (participant) => {
  let participantContainer = document.querySelector(".participant");
  participantContainer.setAttribute("id", participant.sid);

  let tracksContainer = document.createElement("div");
  participantContainer.appendChild(tracksContainer);

  let identityLabel = document.createElement("div");
  identityLabel.setAttribute("class", "label");
  identityLabel.innerHTML = participant.identity;
  participantContainer.appendChild(identityLabel);

  participant.tracks.forEach((publication) => {
    if (publication.isSubscribed)
      trackSubscribed(tracksContainer, publication.track);
  });
  participant.on("trackSubscribed", (track) =>
    trackSubscribed(tracksContainer, track)
  );
  participant.on("trackUnsubscribed", trackUnsubscribed);

  updateParticipantCount();
};

const participantDisconnected = (participant) => {
  document.getElementById(participant.sid).remove();
  updateParticipantCount();
};

const trackSubscribed = (div, track) => {
  let trackElement = track.attach();
  trackElement.addEventListener("click", () => {
    zoomTrack(trackElement);
  });
  div.appendChild(trackElement);
};

const trackUnsubscribed = (track) => {
  track.detach().forEach((element) => {
    if (element.classList.contains("participantZoomed")) {
      zoomTrack(element);
    }
    element.remove();
  });
};

const disconnect = () => {
  room.disconnect();
  while (container.lastChild.id != "local") {
    callContainer.removeChild(container.lastChild);
  }
  joinOrLeave.innerHTML = "Join call";
  connected = false;
  updateParticipantCount();
};

const shareScreenHandler = (event) => {
  event.preventDefault();
  if (!screenTrack) {
    navigator.mediaDevices
      .getDisplayMedia()
      .then((stream) => {
        screenTrack = new Twilio.Video.LocalVideoTrack(stream.getTracks()[0]);
        room.localParticipant.publishTrack(screenTrack);
        screenTrack.mediaStreamTrack.onended = () => {
          shareScreenHandler();
        };
        shareScreenButton.innerHTML = "Stop sharing";
      })
      .catch(() => {
        alert("Could not share the screen.");
      });
  } else {
    room.localParticipant.unpublishTrack(screenTrack);
    screenTrack.stop();
    screenTrack = null;
    shareScreenButton.innerHTML = "Share screen";
  }
};

const zoomTrack = (trackElement) => {
  if (!trackElement.classList.contains("participantZoomed")) {
    // zoom in
    callContainer.childNodes.forEach((participant) => {
      if (participant.className == "participant") {
        participant.childNodes[0].childNodes.forEach((track) => {
          if (track === trackElement) {
            track.classList.add("participantZoomed");
          } else {
            track.classList.add("participantHidden");
          }
        });
        participant.childNodes[1].classList.add("participantHidden");
      }
    });
  } else {
    // zoom out
    classContainer.childNodes.forEach((participant) => {
      if (participant.className == "participant") {
        participant.childNodes[0].childNodes.forEach((track) => {
          if (track === trackElement) {
            track.classList.remove("participantZoomed");
          } else {
            track.classList.remove("participantHidden");
          }
        });
        participant.childNodes[1].classList.remove("participantHidden");
      }
    });
  }
};

const updateParticipantCount = () => {
  if (!connected) count.innerHTML = "Disconnected.";
  else count.innerHTML = room.participants.size + 1 + " participants online.";
};

addLocalVideo();
joinOrLeave.addEventListener("click", connectButtonHandler);
shareScreenButton.addEventListener("click", shareScreenHandler);
