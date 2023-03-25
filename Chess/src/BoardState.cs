using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.NetworkInformation;
using System.Text;
using System.Threading.Tasks;

namespace Chess
{
    internal class BoardState
    {
        private Piece[] configuration;
        private string lastMove;

        private bool whiteKingMoved;
        private bool blackKingMoved;
        private int moveNumber;
        private int turn;

        public BoardState(List<Piece> white_pieces, List<Piece> black_pieces)
        {
            this.configuration = new Piece[64];

            for (int i = 0; i < 64; i++)
            {
                this.configuration[i] = new Piece(PieceType.None, GetSquareFromIndex(i));
            }

            foreach(Piece piece in white_pieces)
            {
                this.configuration[GetIndexOfPositionArray(piece.GetSquare())] = piece;
            }

            foreach (Piece piece in black_pieces)
            {
                this.configuration[GetIndexOfPositionArray(piece.GetSquare())] = piece;
            }

            this.whiteKingMoved = false;
            this.blackKingMoved = false;
            this.moveNumber = 1;
            this.turn = 0;
        }

        public void Move(string moveNotation)
        {
            string square2 = moveNotation;
            if (moveNotation.Count() == 2)
            {
                // this is a pawn move
                int board_index = GetIndexOfPositionArray(square2);

                if(turn == 0)
                {
                    // white's turn
                    for(int i = 1; i <= 2; i++)
                    {
                        if (this.configuration[board_index + (i * 8)].Type == PieceType.White_Pawn)
                        {
                            string square1 = GetSquareFromIndex(board_index + (i * 8));
                            this.Move(square1, square2);
                        }
                    }
                }
                else
                {
                    // black's turn
                    // white's turn
                    for (int i = 1; i <= 2; i++)
                    {
                        if (this.configuration[board_index - (i * 8)].Type == PieceType.Black_Pawn)
                        {
                            string square1 = GetSquareFromIndex(board_index - (i * 8));
                            this.Move(square1, square2);
                        }
                    }
                }
            }
        }

        public void Move(string square1, string square2)
        {
            int from = GetIndexOfPositionArray(square1);
            int to = GetIndexOfPositionArray(square2);

            this.configuration[to].SetPiece(this.configuration[from].Type);
            this.configuration[from].SetPiece(PieceType.None);

            if (this.turn == 1)
            {
                this.moveNumber++;
                this.turn = 0;
            }
            else
            {
                this.turn = 1;
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

        public static string GetSquareFromIndex(int index)
        {
            string res = (char)(65 + (index % 8)) + (8 - (index / 8)).ToString();
            //Debug.WriteLine(index.ToString() + ": " + res);
            return res;
        }

        public static int GetIndexOfPositionArray(string square)
        {
            if (square.Length != 2)
            {
                throw new ArgumentException(square + " must be a chessboard sqaure value.");
            }

            int res = (int)(('8' - square[1]) * 8) + (int)(char.ToUpper(square[0]) - 'A');
            //Debug.WriteLine("square [" + square + "]: " + res.ToString());
            return res;
        }

        public override string ToString()
        {
            StringBuilder ret = new StringBuilder("");

            for(int row = 0; row < 8; row++)
            {
                for (int col = 0; col < 8; col++)
                {
                    ret.Append("[");
                    string square = this.PieceSymbol(this.configuration[(row * 8) + col].Type);
                    ret.Append(square.PadRight(3));
                    ret.Append("] ");
                }
                ret.Append("\n");
            }
            return ret.ToString();
        }

        public void DrawPieces()
        {
            foreach (Piece piece in this.configuration)
            {
                if (piece.Type != PieceType.None)
                {
                    piece.Draw();
                }
            }
        }
    }
}
