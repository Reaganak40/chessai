using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace Chess
{
    internal class PGNReader
    {
        public static void ReadPGN(string PGNPath)
        {
            using (StreamReader file = new StreamReader(PGNPath))
            {
                int counter = 0;
                string ln;

                while ((ln = file.ReadLine()) != null)
                {
                    // If this line is not a comment line, and it is not empty
                    if(!(ln.Length == 0) && (!ln[0].Equals('[') || !ln[ln.Length - 1].Equals(']')))
                    {
                        Debug.WriteLine(ln);
                    }
                    counter++;
                }
            }
        }
    }
}
