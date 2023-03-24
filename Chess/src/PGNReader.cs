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
        public static List<string[]> ReadPGN(string PGNPath)
        {
            List<string[]> moves = new List<string[]>{}; 
            using (StreamReader file = new StreamReader(PGNPath))
            {
                int counter = 0;
                string ln;


                while ((ln = file.ReadLine()) != null)
                {
                    // If this line is not a comment line, and it is not empty
                    if(!(ln.Length == 0) && (!ln[0].Equals('[') || !ln[ln.Length - 1].Equals(']')))
                    {
                        string[] strings = ln.Split(' ');

                        int index = 0;

                        while (index < strings.Length)
                        {
                            string white_move = strings[index + 1];
                            string black_move = strings[index + 2];
                            moves.Add(new string[] { white_move, black_move });
                            index += 3;
                        }
                    }
                    counter++;
                }
                Debug.WriteLine("Moves: ");
                int move_num = 1;
                foreach (var move in moves)
                {
                    Debug.WriteLine(move_num + ". " + move[0] + ", " + move[1]);
                    move_num++;
                }
            }

            return moves;
        }
    }
}
