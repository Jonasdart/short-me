SELECT 
    name,
    requested_name,
    short_name,
    created_at,
    expire_at
FROM 
    urls
WHERE 
    short_name = '{shortName}'