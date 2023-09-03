<h1>Description</h1>
This program intends to provide a dynamic domain name system (DDNS) service to users of Porkbun or Clourflare with a <strong>single</strong> IP. The purpose of this program is to periodically check the type A records of your DNS provider and make sure they match your actual IP. If they do not, this program will make the appropriate API calls to update it.
<br><br>
Upon a single envokation the program simply compares the current IP address to the address stored in the provider's type A records. If they do not match, the program updates the A records with the new IP. This program is intended to be run with a job scheduler such as <code>cron</code>.
<br><br>
<h1>Dependencies</h1>
<ul>
    <li>Python3 <br></li>
    <li>Porkbun or Cloudflare nameservers <br></li>
    <li>Job scheduler, such as <code>cron</code><br></li>
</ul>
<br>


<h1>Setup</h1>
<ol>
    <li>Download source</li>
    <li>Edit config.json</li>
        <ul>
            <li>Using Porkbun Nameservers</li>
            <ol>
                <li>Generate your API keys at <a>https://porkbun.com/account/api</a></li>
                <li>Set PORKBUN_API_KEY with API Key</li>
                    <ul><li>Should look like <code>pk1_...</code></li></ul>
                <li>Set PORKBUN_API_SECRET with Secret Key</li>
                    <ul><li>Should look like <code>sk1_...</code></li></ul>
            </ol>
            <li>Using Cloudlfare Nameservers</li>
            <ol>
                <li>Create an API Token</li>
                <ol>
                    <li>Visit <a>https://dash.cloudflare.com/profile/api-tokens</a></li>
                    <li>Create token</li>
                    <li>Use the "Edit zone DNS" template</li>
                    <ol>
                        <li>Set permissions to <code>Zone</code>, <code>DNS</code>, <code>Edit</code></li>
                        <li>Set Resources to <code>Include</code>, <code>Specific zone</code>, <code>example.com</code></li>
                        <li>Continue to Summary</li>
                        <li>Create Token</li>
                    </ol>
                </ol>
                <li>Set CLOUFLARE_TOKEN with the User API Token</li>
                <li>Set CLOUDFLARE_ZONE_ID</li>
                    <ul><li>Refer to <a>https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/</a></li></ul>
                <li>Set CLOUFLARE_ACCOUNT_ID</li>
                    <ul><li>Refer to <a>https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/</a></li></ul>
            </ol>
        </ul>
    <li>Schedule execution</li>
    <ul>
        <li>Using <code>cron</code></li>
        <ol>
            <li>Edit launch_cron_job.sh</li>
            <ul>
                <li>edit PYTHONPATH as necessary</li>
                <li>edit LOGPATH if desired</li>
                <li>you may add or remove options as desired</li>
                <ul>
                    <li>run with <code>--help</code> to view options</li>
                </ul>
            </ul>
            <li>Run launch_cron_job.sh</li>
            <ul>
                <li><code>chmod +x ./launch_cron_job.sh</code></li>
                <li><code>.\launch_cron_job.sh</code></li>
            </ul>
            <li>Confirm the job is running</li>
            <ul>
                <li><code>crontab -l</code></li>
                <ul>
                    <li>may need to specify <code>-u USER</code></li>
                </ul>
            </ul>
        </ol>
</ol>