using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Pipes;
using System.Threading.Tasks;
using Flow.Launcher.Plugin;

namespace Flow.Launcher.Plugin.komoflow
{
    public class komoflow : IPlugin
    {
        private PluginInitContext _context;

        public void Init(PluginInitContext context)
        {
            _context = context;
            StartNamedPipeServer();
        }

        public List<Result> Query(Query query)
        {
            return new List<Result>();
        }

        private void StartNamedPipeServer()
        {
            Task.Run(() =>
            {
                using (var pipeServer = new NamedPipeServerStream("komorebi-pipe"))
                {
                    Console.WriteLine("Waiting for connection.");
                    pipeServer.WaitForConnection();
                    Console.WriteLine("Client connected.");
                    using (var sr = new StreamReader(pipeServer))
                    {
                        
                    }
                }
            });
        }
    }
}
