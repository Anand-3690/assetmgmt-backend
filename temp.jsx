{asset.documents.length > 0 && (
        <>
          <h3>Documents</h3>
          <ul>
            {asset.documents.map((d) => (
              <li key={d.id}>
                <a href={d.url} target="_blank" rel="noreferrer">{d.doc_type}</a>
                {!d.is_public && <span style={{ color: '#888', fontSize: 12 }}> (private)</span>}
              </li>
            ))}
          </ul>
        </>
      )}