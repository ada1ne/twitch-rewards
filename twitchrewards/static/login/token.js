const parsedHash = new URLSearchParams(
    window.location.search
);

const code = parsedHash.get("code");
const data = { code: code };
fetch("/token", { method: "POST", body: JSON.stringify(data), headers: { "Content-Type": "application/json" } })
    .then((response) => {
        if (!response.ok) {
            alert('Algo deu errado. Avisa no Discord!');
        }
        else {
            window.location.href = '/';
        }
    });
