using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Chess
{
    internal class BoardState
    {
        private PieceType[] configuration;
        private string lastMove;
        private int moveNumber;

        private bool whiteKingMoved;
        private bool blackKingMoved;

        public BoardState(PieceType[] customConfiguration = null, string lastMove = null, int moveNumber = 0)
        {
            if (!(customConfiguration is null))
            {
                this.configuration = customConfiguration;
            }
            else
            {
                this.configuration = new PieceType[64];

                for (int i = 16; i < 48; i++)
                {
                    this.configuration[i] = PieceType.None;
                }

                this.configuration[0] = PieceType.Black_Rook;
                this.configuration[1] = PieceType.Black_Knight;
                this.configuration[2] = PieceType.Black_Bishop;
                this.configuration[3] = PieceType.Black_Queen;
                this.configuration[4] = PieceType.Black_King;
                this.configuration[5] = PieceType.Black_Bishop;
                this.configuration[6] = PieceType.Black_Knight;
                this.configuration[7] = PieceType.Black_Rook;

                for (int i = 8; i < 16; i++)
                {
                    this.configuration[i] = PieceType.Black_Pawn;
                }

                this.configuration[56] = PieceType.White_Rook;
                this.configuration[57] = PieceType.White_Knight;
                this.configuration[58] = PieceType.White_Bishop;
                this.configuration[59] = PieceType.White_Queen;
                this.configuration[60] = PieceType.White_King;
                this.configuration[61] = PieceType.White_Bishop;
                this.configuration[62] = PieceType.White_Knight;
                this.configuration[63] = PieceType.White_Rook;

                for (int i = 48; i < 56; i++)
                {
                    this.configuration[i] = PieceType.White_Pawn;
                }
            }

            if (!(lastMove is null))
            {
                this.lastMove = lastMove;
            }
            else
            {
                this.lastMove = string.Empty;
            }

            this.moveNumber = moveNumber;
        }

        public void Move(string square1, string square2)
        {
            Debug.WriteLine(Piece.GetIndexOfPositionArray(square1) + " to " + Piece.GetIndexOfPositionArray(square2));
            PieceType pieceOnSquare1 = this.configuration[Piece.GetIndexOfPositionArray(square1)];
            this.configuration[Piece.GetIndexOfPositionArray(square2)] = pieceOnSquare1;
            this.configuration[Piece.GetIndexOfPositionArray(square1)] = PieceType.None;

            this.moveNumber++;
        }

        public PieceType[] Configuration
        {
            get
            {
                return this.configuration;
            }

            set
            {
                this.configuration = value;
            }
        }

        public bool WhiteTurn
        {
            get
            {
                return this.moveNumber % 2 == 0;
            }
        }

        private string PieceSymbol(PieceType type)
        {
            switch (type)
            {
                case PieceType.White_King:
                    return "WK";
                case PieceType.White_Queen:
                    return "WQ";
                case PieceType.White_Bishop:
                    return "WB";
                case PieceType.White_Knight:
                    return "WKN";
                case PieceType.White_Rook:
                    return "WR";
                case PieceType.White_Pawn:
                    return "WP";
                case PieceType.Black_King:
                    return "BK";
                case PieceType.Black_Queen:
                    return "BQ";
                case PieceType.Black_Bishop:
                    return "BB";
                case PieceType.Black_Knight:
                    return "BKN";
                case PieceType.Black_Rook:
                    return "BR";
                case PieceType.Black_Pawn:
                    return "BP";
                default:
                    return "___";

            }
        }

        public override string ToString()
        {
            StringBuilder ret = new StringBuilder("");

            for(int row = 0; row < 8; row++)
            {
                for (int col = 0; col < 8; col++)
                {
                    ret.Append("[");
                    string square = this.PieceSymbol(this.configuration[(row * 8) + col]);
                    ret.Append(square.PadRight(3));
                    ret.Append("] ");
                }
                ret.Append("\n");
            }
            return ret.ToString();
        }
    }
}
