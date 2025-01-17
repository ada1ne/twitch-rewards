const parsedHash = new URLSearchParams(
    window.location.hash.substring(1)
);

const access_token = parsedHash.get("access_token");
const data = { twitch_token: access_token };
fetch("/token", { method: "POST", body: JSON.stringify(data), headers: { "Content-Type": "application/json" } })
    .then((response) => {
        if (!response.ok) {
            alert('Algo deu errado. Avisa no Discord!');
        }
        else {
            window.location.href = '/';
        }
    });
