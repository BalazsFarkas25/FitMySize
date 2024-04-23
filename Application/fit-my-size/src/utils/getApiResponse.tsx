async function getApiResponse(blobImg: string|null) {
    const response = await fetch('http://localhost:3001/getSize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ blob: blobImg })
      });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    } else {
        const data = await response.json();
        return data['prediction']
    }
}
export default getApiResponse;
